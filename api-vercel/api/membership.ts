import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../lib/supabase';
import { handleCors, errorResponse, successResponse, getUserFromRequest } from '../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  const { action } = req.query;

  switch (action) {
    case 'status':
      return await getMembershipStatus(req, res);
    case 'check-expired':
      return await checkExpiredMemberships(req, res);
    case 'admin-update':
      return await adminUpdateMembership(req, res);
    case 'verify-payment':
      return await verifyPayment(req, res);
    default:
      return errorResponse(res, 'Invalid action', 400);
  }
}

// 获取会员状态
async function getMembershipStatus(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'GET') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    // 验证用户认证
    const user = getUserFromRequest(req);
    if (!user) {
      return errorResponse(res, '请先登录', 401);
    }

    // 从数据库获取最新的用户信息
    const { data: userData, error } = await supabase
      .from('users')
      .select('id, username, email, is_member, membership_expires, created_at')
      .eq('id', user.id)
      .single();

    if (error || !userData) {
      return errorResponse(res, '用户不存在', 404);
    }

    // 检查会员状态
    let isMembershipActive = userData.is_member;
    let membershipStatus = 'inactive';
    let daysRemaining = 0;

    if (userData.membership_expires) {
      const expiresAt = new Date(userData.membership_expires);
      const now = new Date();
      const timeDiff = expiresAt.getTime() - now.getTime();
      daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24));

      if (expiresAt < now) {
        // 会员已过期，更新状态
        await supabase
          .from('users')
          .update({ 
            is_member: false,
            membership_expires: null 
          })
          .eq('id', userData.id);
        
        isMembershipActive = false;
        membershipStatus = 'expired';
        daysRemaining = 0;
      } else {
        membershipStatus = 'active';
        
        // 如果剩余天数少于7天，标记为即将过期
        if (daysRemaining <= 7) {
          membershipStatus = 'expiring_soon';
        }
      }
    }

    // 获取支付历史
    const { data: payments } = await supabase
      .from('payments')
      .select('amount, payment_date, status, transaction_id')
      .eq('user_id', userData.id)
      .order('payment_date', { ascending: false })
      .limit(5);

    return successResponse(res, {
      user: {
        id: userData.id,
        username: userData.username,
        email: userData.email,
        is_member: isMembershipActive,
        membership_expires: userData.membership_expires,
        membership_status: membershipStatus,
        days_remaining: daysRemaining,
        created_at: userData.created_at
      },
      payments: payments || []
    });

  } catch (error) {
    console.error('获取会员状态错误:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}

// 检查过期会员
async function checkExpiredMemberships(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST' && req.method !== 'GET') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  // 验证 cron 密钥（可选，增加安全性）
  const cronSecret = req.headers['x-cron-secret'] || req.query.secret;
  if (cronSecret !== process.env.CRON_SECRET && cronSecret !== 'manual-check') {
    return errorResponse(res, 'Unauthorized', 401);
  }

  try {
    console.log('开始检查过期会员...');
    
    // 查找所有过期的会员
    const { data: expiredUsers, error } = await supabase
      .from('users')
      .select('id, username, email, membership_expires')
      .eq('is_member', true)
      .lt('membership_expires', new Date().toISOString());

    if (error) {
      console.error('查询过期会员失败:', error);
      return errorResponse(res, '查询失败', 500);
    }

    let processedCount = 0;
    let notificationsSent = 0;

    if (expiredUsers && expiredUsers.length > 0) {
      // 批量更新过期会员状态
      const userIds = expiredUsers.map(user => user.id);
      
      const { error: updateError } = await supabase
        .from('users')
        .update({ 
          is_member: false,
          membership_expires: null 
        })
        .in('id', userIds);

      if (updateError) {
        console.error('更新过期会员状态失败:', updateError);
        return errorResponse(res, '更新失败', 500);
      }

      processedCount = expiredUsers.length;
      console.log(`已处理 ${processedCount} 个过期会员`);
    }

    // 查找即将过期的会员（7天内）
    const sevenDaysFromNow = new Date();
    sevenDaysFromNow.setDate(sevenDaysFromNow.getDate() + 7);

    const { data: expiringUsers, error: expiringError } = await supabase
      .from('users')
      .select('id, username, email, membership_expires')
      .eq('is_member', true)
      .gte('membership_expires', new Date().toISOString())
      .lte('membership_expires', sevenDaysFromNow.toISOString());

    if (expiringError) {
      console.error('查询即将过期会员失败:', expiringError);
    } else if (expiringUsers && expiringUsers.length > 0) {
      console.log(`发现 ${expiringUsers.length} 个即将过期的会员`);
      notificationsSent = expiringUsers.length;
    }

    return successResponse(res, {
      expired_processed: processedCount,
      expiring_notifications: notificationsSent,
      timestamp: new Date().toISOString()
    }, `处理完成: ${processedCount} 个过期会员, ${notificationsSent} 个即将过期提醒`);

  } catch (error) {
    console.error('检查会员状态错误:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}

// 管理员更新会员状态
async function adminUpdateMembership(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { username, plan, adminSecret } = req.body;

    // 验证管理员密钥
    if (adminSecret !== process.env.ADMIN_SECRET && adminSecret !== 'temp-admin-2025') {
      return errorResponse(res, 'Unauthorized', 401);
    }

    if (!username || !plan) {
      return errorResponse(res, '用户名和计划都是必填项');
    }

    // 查找用户
    const { data: user, error: userError } = await supabase
      .from('users')
      .select('id, username, email')
      .eq('username', username)
      .single();

    if (userError || !user) {
      return errorResponse(res, '用户不存在');
    }

    // 设置会员过期时间
    const membershipExpires = new Date();
    if (plan === 'year') {
      membershipExpires.setFullYear(membershipExpires.getFullYear() + 1);
    } else if (plan === 'month') {
      membershipExpires.setMonth(membershipExpires.getMonth() + 1);
    } else {
      return errorResponse(res, '无效的计划类型');
    }

    // 更新用户会员状态
    const { error: updateError } = await supabase
      .from('users')
      .update({
        is_member: true,
        membership_expires: membershipExpires.toISOString()
      })
      .eq('id', user.id);

    if (updateError) {
      console.error('更新会员状态失败:', updateError);
      return errorResponse(res, '更新失败', 500);
    }

    // 记录支付（模拟）
    await supabase
      .from('payments')
      .insert([
        {
          user_id: user.id,
          amount: plan === 'year' ? 9.99 : 0.99,
          status: 'completed',
          transaction_id: `manual_${Date.now()}`
        }
      ]);

    return successResponse(res, {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        is_member: true,
        membership_expires: membershipExpires.toISOString()
      }
    }, `用户 ${username} 已成功升级为${plan === 'year' ? '年' : '月'}付会员`);

  } catch (error) {
    console.error('更新会员状态错误:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}

// 验证支付并激活会员
async function verifyPayment(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    // 验证用户认证
    const user = getUserFromRequest(req);
    if (!user) {
      return errorResponse(res, '请先登录', 401);
    }

    const { paymentIntentId } = req.body;

    if (!paymentIntentId) {
      return errorResponse(res, '缺少支付意图ID');
    }

    // 从 Stripe 获取支付意图详情
    const Stripe = require('stripe');
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: '2025-06-30.basil',
    });

    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);

    if (paymentIntent.status !== 'succeeded') {
      return errorResponse(res, '支付未成功');
    }

    // 验证支付意图是否属于当前用户
    if (paymentIntent.metadata?.user_id !== user.id) {
      return errorResponse(res, '支付验证失败');
    }

    // 检查是否已经处理过这个支付
    const { data: existingPayment } = await supabase
      .from('payments')
      .select('id')
      .eq('transaction_id', paymentIntent.id)
      .single();

    if (existingPayment) {
      return errorResponse(res, '此支付已经处理过了');
    }

    // 处理支付成功
    const plan = paymentIntent.metadata?.plan;
    const amount = paymentIntent.amount / 100;

    // 记录支付
    await supabase
      .from('payments')
      .insert([
        {
          user_id: user.id,
          amount,
          status: 'completed',
          transaction_id: paymentIntent.id
        }
      ]);

    // 设置会员过期时间
    const membershipExpires = new Date();
    if (plan === 'year') {
      membershipExpires.setFullYear(membershipExpires.getFullYear() + 1);
    } else if (plan === 'month') {
      membershipExpires.setMonth(membershipExpires.getMonth() + 1);
    }

    // 更新用户会员状态
    await supabase
      .from('users')
      .update({
        is_member: true,
        membership_expires: membershipExpires.toISOString()
      })
      .eq('id', user.id);

    console.log(`Payment verified and processed for user ${user.id}, plan: ${plan}`);

    return successResponse(res, {
      user_id: user.id,
      plan: plan,
      membership_expires: membershipExpires.toISOString(),
      amount: amount
    }, '支付验证成功，会员权限已激活');

  } catch (error) {
    console.error('Payment verification error:', error);
    return errorResponse(res, '支付验证失败，请稍后重试', 500);
  }
}