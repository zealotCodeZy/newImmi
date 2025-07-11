import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../lib/supabase';
import { handleCors, verifyPassword, generateToken, errorResponse, successResponse } from '../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { username, password } = req.body;

    // 验证输入
    if (!username || !password) {
      return errorResponse(res, '用户名和密码都是必填项');
    }

    // 查找用户
    const { data: user, error } = await supabase
      .from('users')
      .select('*')
      .eq('username', username)
      .single();

    if (error || !user) {
      return errorResponse(res, '用户名或密码错误');
    }

    // 验证密码
    const isValidPassword = await verifyPassword(password, user.password_hash);
    if (!isValidPassword) {
      return errorResponse(res, '用户名或密码错误');
    }

    // 检查会员状态
    let isMembershipActive = user.is_member;
    if (user.membership_expires && new Date(user.membership_expires) < new Date()) {
      // 会员已过期，更新状态
      await supabase
        .from('users')
        .update({ is_member: false })
        .eq('id', user.id);
      isMembershipActive = false;
    }

    // 生成 JWT token
    const token = generateToken({
      id: user.id,
      username: user.username,
      email: user.email
    });

    return successResponse(res, {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        is_member: isMembershipActive,
        membership_expires: user.membership_expires
      },
      token
    }, '登录成功');

  } catch (error) {
    console.error('Login error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 