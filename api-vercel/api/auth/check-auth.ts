import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../lib/supabase';
import { handleCors, verifyToken, errorResponse, successResponse } from '../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'GET') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return errorResponse(res, '未提供认证令牌', 401);
    }

    const token = authHeader.substring(7);
    const decoded = verifyToken(token);

    if (!decoded) {
      return errorResponse(res, '无效的认证令牌', 401);
    }

    // 从数据库获取最新的用户信息
    const { data: user, error } = await supabase
      .from('users')
      .select('id, username, email, is_member, membership_expires')
      .eq('id', decoded.id)
      .single();

    if (error || !user) {
      return errorResponse(res, '用户不存在', 404);
    }

    return successResponse(res, {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        is_member: user.is_member,
        membership_expires: user.membership_expires
      }
    }, '认证成功');

  } catch (error) {
    console.error('Auth check error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 