import { VercelRequest, VercelResponse } from '@vercel/node';
import { supabase } from '../../../lib/supabase';
import { handleCors, errorResponse, successResponse } from '../../../lib/utils';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (handleCors(req, res)) return;

  if (req.method !== 'GET') {
    return errorResponse(res, 'Method not allowed', 405);
  }

  try {
    const { address } = req.query;

    if (!address) {
      return errorResponse(res, '地址参数是必填项');
    }

    // 根据地址查询租房信息
    const { data, error } = await supabase
      .from('rent_info')
      .select('*')
      .ilike('address', `%${address}%`)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error) {
      if (error.code === 'PGRST116') {
        return errorResponse(res, '未找到相关信息', 404);
      }
      console.error('Database error:', error);
      return errorResponse(res, '获取租房信息失败');
    }

    return successResponse(res, data, '获取成功');

  } catch (error) {
    console.error('Get rent detail error:', error);
    return errorResponse(res, '服务器错误，请稍后重试', 500);
  }
} 