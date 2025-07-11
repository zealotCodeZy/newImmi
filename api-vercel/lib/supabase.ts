import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

// 使用 service role key 来绕过 RLS (Row Level Security)
export const supabase = createClient(supabaseUrl, supabaseServiceKey);

// 类型定义
export interface User {
  id: string;
  username: string;
  email: string;
  password_hash: string;
  created_at: string;
  is_member: boolean;
  membership_expires?: string;
}

export interface Payment {
  id: string;
  user_id: string;
  amount: number;
  payment_date: string;
  status: 'pending' | 'completed' | 'failed';
  transaction_id: string;
}

export interface RentInfo {
  id: string;
  zipcode: string;
  address?: string;
  content: string;
  created_at: string;
}

export interface WorkInfo {
  id: string;
  name?: string;
  zipcode?: string;
  address?: string;
  content: string;
  created_at: string;
} 