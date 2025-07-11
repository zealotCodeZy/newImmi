import { NextApiRequest, NextApiResponse } from 'next';
import { supabase } from '../../lib/supabase';
import { handleCors, getUserFromRequest, errorResponse, successResponse } from '../../lib/utils';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (handleCors(req, res)) return;

  switch (req.method) {
    case 'GET':
      return await getRentInfo(req, res);
    case 'POST':
      return await createRentInfo(req, res);
    default:
      return errorResponse(res, 'Method not allowed', 405);
  }
}

// 获取租房信息
async function getRentInfo(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { zipcode } = req.query;

    let query = supabase
      .from('rent_info')
      .select('*')
      .order('created_at', { ascending: false });

    // 如果指定了邮编，则过滤
    if (zipcode) {
      query = query.eq('zipcode', zipcode);
    }

    const { data, error } = await query;

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '获取租房信息失败');
    }

    return successResponse(res, data, '获取成功');

  } catch (error) {
    console.error('Get rent info error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}

// 创建租房信息
async function createRentInfo(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 验证用户权限
    const user = getUserFromRequest(req);
    if (!user) {
      return errorResponse(res, '请先登录', 401);
    }

    const { zipcode, address, content } = req.body;

    // 验证输入
    if (!zipcode || !content) {
      return errorResponse(res, '邮编和内容都是必填项');
    }

    // 创建租房信息
    const { data, error } = await supabase
      .from('rent_info')
      .insert([
        {
          zipcode,
          address,
          content
        }
      ])
      .select()
      .single();

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '创建租房信息失败');
    }

    return successResponse(res, data, '创建成功');

  } catch (error) {
    console.error('Create rent info error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 