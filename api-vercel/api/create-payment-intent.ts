import { VercelRequest, VercelResponse } from '@vercel/node';
import Stripe from 'stripe';
import { handleCors, errorResponse, successResponse } from '../lib/utils';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
});

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { plan, userId } = req.body;

    if (!plan) {
      return errorResponse(res, '请选择会员计划');
    }

    // 根据计划设置价格
    let amount: number;
    let description: string;
    
    if (plan === 'year') {
      amount = 999; // $9.99 in cents
      description = '年付会员 - 新移民防踩坑';
    } else if (plan === 'month') {
      amount = 99; // $0.99 in cents
      description = '月付会员 - 新移民防踩坑';
    } else {
      return errorResponse(res, '无效的会员计划');
    }

    // 创建支付意图
    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency: 'usd',
      description,
      metadata: {
        user_id: userId || 'anonymous',
        plan: plan
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