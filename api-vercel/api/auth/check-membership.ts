import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../lib/supabase';
import { handleCors, errorResponse, successResponse, getUserFromRequest } from '../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

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
      .select('id, username, email, is_member, membership_expires')
      .eq('id', user.id)
      .single();

    if (error || !userData) {
      return errorResponse(res, '用户不存在', 404);
    }

    // 检查会员状态
    let isMembershipActive = userData.is_member;
    if (userData.membership_expires && new Date(userData.membership_expires) < new Date()) {
      // 会员已过期，更新状态
      await supabase
        .from('users')
        .update({ is_member: false })
        .eq('id', userData.id);
      isMembershipActive = false;
    }

    return successResponse(res, {
      user: {
        id: userData.id,
        username: userData.username,
        email: userData.email,
        is_member: isMembershipActive,
        membership_expires: userData.membership_expires
      },
      authenticated: true
    });

  } catch (error) {
    console.error('Check membership error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}