import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../../lib/supabase';
import { handleCors, errorResponse, successResponse } from '../../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'GET') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { name } = req.query;

    if (!name) {
      return errorResponse(res, '公司名称参数是必填项');
    }

    // 根据公司名称查询工作信息
    const { data, error } = await supabase
      .from('work_info')
      .select('*')
      .ilike('name', `%${name}%`)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Database error:', error);
      return errorResponse(res, '获取工作信息失败');
    }

    if (!data || data.length === 0) {
      return errorResponse(res, '未找到相关信息', 404);
    }

    return successResponse(res, { companies: data }, '获取成功');

  } catch (error) {
    console.error('Get work detail error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 