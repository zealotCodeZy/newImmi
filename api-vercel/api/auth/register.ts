import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../lib/supabase';
import { handleCors, hashPassword, generateToken, errorResponse, successResponse } from '../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'POST') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { username, email, password } = req.body;

    // 验证输入
    if (!username || !email || !password) {
      return errorResponse(res, '用户名、邮箱和密码都是必填项');
    }

    if (password.length < 6) {
      return errorResponse(res, '密码长度至少6位');
    }

    // 检查用户名是否已存在
    const { data: existingUser } = await supabase
      .from('users')
      .select('id')
      .eq('username', username)
      .single();

    if (existingUser) {
      return errorResponse(res, '用户名已存在');
    }

    // 检查邮箱是否已存在
    const { data: existingEmail } = await supabase
      .from('users')
      .select('id')
      .eq('email', email)
      .single();

    if (existingEmail) {
      return errorResponse(res, '邮箱已被注册');
    }

    // 加密密码
    const passwordHash = await hashPassword(password);

    // 创建用户
    const { data: newUser, error } = await supabase
      .from('users')
      .insert([
        {
          username,
          email,
          password_hash: passwordHash,
          is_member: false
        }
      ])
      .select()
      .single();

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '注册失败，请稍后重试');
    }

    // 生成 JWT token
    const token = generateToken({
      id: newUser.id,
      username: newUser.username,
      email: newUser.email
    });

    return successResponse(res, {
      user: {
        id: newUser.id,
        username: newUser.username,
        email: newUser.email,
        is_member: newUser.is_member
      },
      token
    }, '注册成功');

  } catch (error) {
    console.error('Registration error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 