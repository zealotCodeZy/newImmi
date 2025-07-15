import { VercelRequest, VercelResponse } from '@vercel/node';
import Stripe from 'stripe';
import { supabase } from '../../lib/supabase';
import { errorResponse, successResponse } from '../../lib/utils';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
});

const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  const sig = req.headers['stripe-signature'] as string;
  
  // 记录 webhook 调用
  console.log('Webhook called:', {
    signature: sig ? 'present' : 'missing',
    body_length: req.body ? req.body.length : 0,
    headers: Object.keys(req.headers)
  });

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    console.log('Webhook event verified:', event.type, event.id);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return errorResponse(res, 'Webhook signature verification failed', 400);
  }

  try {
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentIntentSucceeded(event.data.object as Stripe.PaymentIntent);
        break;
      case 'checkout.session.completed':
        await handleCheckoutSessionCompleted(event.data.object as Stripe.Checkout.Session);
        break;
      case 'invoice.payment_succeeded':
        await handleInvoicePaymentSucceeded(event.data.object as Stripe.Invoice);
        break;
      case 'invoice.payment_failed':
        await handleInvoicePaymentFailed(event.data.object as Stripe.Invoice);
        break;
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return successResponse(res, { received: true });
  } catch (error) {
    console.error('Webhook handler error:', error);
    return errorResponse(res, 'Webhook handler failed', 500);
  }
}

async function handlePaymentIntentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  if (paymentIntent.status === 'succeeded' && paymentIntent.metadata?.user_id) {
    const userId = paymentIntent.metadata.user_id;
    const plan = paymentIntent.metadata.plan;
    const amount = paymentIntent.amount / 100; // Convert from cents to dollars

    // 记录支付
    await supabase
      .from('payments')
      .insert([
        {
          user_id: userId,
          amount,
          status: 'completed',
          transaction_id: paymentIntent.id
        }
      ]);

    // 根据计划设置会员过期时间
    const membershipExpires = new Date();
    if (plan === 'year') {
      membershipExpires.setFullYear(membershipExpires.getFullYear() + 1); // 1年会员
    } else if (plan === 'month') {
      membershipExpires.setMonth(membershipExpires.getMonth() + 1); // 1个月会员
    }

    // 更新用户会员状态
    await supabase
      .from('users')
      .update({
        is_member: true,
        membership_expires: membershipExpires.toISOString()
      })
      .eq('id', userId);

    console.log(`User ${userId} became member with plan ${plan} until ${membershipExpires.toISOString()}`);
  }
}

async function handleCheckoutSessionCompleted(session: Stripe.Checkout.Session) {
  if (session.payment_status === 'paid' && session.metadata?.user_id) {
    const userId = session.metadata.user_id;
    const amount = session.amount_total ? session.amount_total / 100 : 0;

    // 记录支付
    await supabase
      .from('payments')
      .insert([
        {
          user_id: userId,
          amount,
          status: 'completed',
          transaction_id: session.id
        }
      ]);

    // 更新用户会员状态
    const membershipExpires = new Date();
    membershipExpires.setMonth(membershipExpires.getMonth() + 1); // 1个月会员

    await supabase
      .from('users')
      .update({
        is_member: true,
        membership_expires: membershipExpires.toISOString()
      })
      .eq('id', userId);
  }
}

async function handleInvoicePaymentSucceeded(invoice: Stripe.Invoice) {
  if ((invoice as any).subscription && invoice.customer) {
    // 处理订阅续费
    const customer = await stripe.customers.retrieve(invoice.customer as string) as Stripe.Customer;
    if (customer.metadata?.user_id) {
      const userId = customer.metadata.user_id;
      const membershipExpires = new Date();
      membershipExpires.setMonth(membershipExpires.getMonth() + 1);

      await supabase
        .from('users')
        .update({
          is_member: true,
          membership_expires: membershipExpires.toISOString()
        })
        .eq('id', userId);
    }
  }
}

async function handleInvoicePaymentFailed(invoice: Stripe.Invoice) {
  if (invoice.customer) {
    const customer = await stripe.customers.retrieve(invoice.customer as string) as Stripe.Customer;
    if (customer.metadata?.user_id) {
      const userId = customer.metadata.user_id;

      // 支付失败，取消会员状态
      await supabase
        .from('users')
        .update({ is_member: false })
        .eq('id', userId);
    }
  }
} 