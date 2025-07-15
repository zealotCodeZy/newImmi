import { VercelRequest, VercelResponse } from '@vercel/node';
import Stripe from 'stripe';
import { supabase } from '../lib/supabase';
import { handleCors, errorResponse, successResponse, getUserFromRequest } from '../lib/utils';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
});

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    // 验证用户认证
    const user = getUserFromRequest(req);
    if (!user) {
      return errorResponse(res, '请先登录', 401);
    }

    const { plan } = req.body;

    if (!plan) {
      return errorResponse(res, '请选择会员计划');
    }

    // 检查用户是否已经是会员
    const { data: userData } = await supabase
      .from('users')
      .select('is_member, membership_expires')
      .eq('id', user.id)
      .single();

    if (userData?.is_member && userData.membership_expires) {
      const expiresAt = new Date(userData.membership_expires);
      if (expiresAt > new Date()) {
        return errorResponse(res, '您已经是会员，无需重复购买');
      }
    }

    // 根据计划设置价格
    let amount: number;
    let description: string;
    
    if (plan === 'year') {
      amount = 999; // $9.99 in cents
      description = '年付会员 - 新移民防踩坑 (12个月)';
    } else if (plan === 'month') {
      amount = 99; // $0.99 in cents
      description = '月付会员 - 新移民防踩坑 (1个月)';
    } else {
      return errorResponse(res, '无效的会员计划');
    }

    // 创建或获取客户
    let customer;
    const { data: existingPayment } = await supabase
      .from('payments')
      .select('transaction_id')
      .eq('user_id', user.id)
      .limit(1)
      .single();

    if (existingPayment) {
      // 尝试从之前的支付中获取客户信息
      try {
        const paymentIntent = await stripe.paymentIntents.retrieve(existingPayment.transaction_id);
        if (paymentIntent.customer) {
          customer = await stripe.customers.retrieve(paymentIntent.customer as string);
        }
      } catch (e) {
        // 忽略错误，创建新客户
      }
    }

    if (!customer) {
      // 创建新客户
      customer = await stripe.customers.create({
        email: user.email,
        metadata: {
          user_id: user.id,
          username: user.username
        }
      });
    }

    // 创建支付意图
    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency: 'usd',
      description,
      customer: customer.id,
      metadata: {
        user_id: user.id,
        plan: plan,
        username: user.username,
        email: user.email
      },
      automatic_payment_methods: {
        enabled: true,
      },
    });

    return successResponse(res, {
      clientSecret: paymentIntent.client_secret,
      publishableKey: process.env.STRIPE_PUBLISHABLE_KEY
    });

  } catch (error) {
    console.error('Payment intent creation error:', error);
    return errorResponse(res, '创建支付失败，请稍后重试', 500);
  }
} 