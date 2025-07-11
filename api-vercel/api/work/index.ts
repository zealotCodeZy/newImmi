import { NextApiRequest, NextApiResponse } from 'next';
import { supabase } from '../../lib/supabase';
import { handleCors, getUserFromRequest, errorResponse, successResponse } from '../../lib/utils';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (handleCors(req, res)) return;

  switch (req.method) {
    case 'GET':
      return await getWorkInfo(req, res);
    case 'POST':
      return await createWorkInfo(req, res);
    default:
      return errorResponse(res, 'Method not allowed', 405);
  }
}

// 获取工作信息
async function getWorkInfo(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { zipcode } = req.query;

    let query = supabase
      .from('work_info')
      .select('*')
      .order('created_at', { ascending: false });

    // 如果指定了邮编，则过滤
    if (zipcode) {
      query = query.eq('zipcode', zipcode);
    }

    const { data, error } = await query;

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '获取工作信息失败');
    }

    return successResponse(res, data, '获取成功');

  } catch (error) {
    console.error('Get work info error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
}

// 创建工作信息
async function createWorkInfo(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 验证用户权限
    const user = getUserFromRequest(req);
    if (!user) {
      return errorResponse(res, '请先登录', 401);
    }

    const { name, zipcode, address, content } = req.body;

    // 验证输入
    if (!content) {
      return errorResponse(res, '内容为必填项');
    }

    // 创建工作信息
    const { data, error } = await supabase
      .from('work_info')
      .insert([
        {
          name,
          zipcode,
          address,
          content
        }
      ])
      .select()
      .single();

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '创建工作信息失败');
    }

    return successResponse(res, data, '创建成功');

  } catch (error) {
    console.error('Create work info error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 