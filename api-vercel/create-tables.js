const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://wbjbnfogbsiwqwnopocn.supabase.co';
const supabaseServiceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndiamJuZm9nYnNpd3F3bm9wb2NuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjI0Njk2MywiZXhwIjoyMDY3ODIyOTYzfQ.qgo76VLXsnXKfpxeTyYA7t76QIlEpsC4b5jv8HdY5ro';

const supabase = createClient(supabaseUrl, supabaseServiceKey);

const createTablesSQL = `
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_member BOOLEAN DEFAULT FALSE,
    membership_expires TIMESTAMP WITH TIME ZONE
);

-- 创建支付记录表
CREATE TABLE IF NOT EXISTS payments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
    transaction_id TEXT UNIQUE
);

-- 创建租房信息表
CREATE TABLE IF NOT EXISTS rent_info (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    zipcode TEXT NOT NULL,
    address TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建工作信息表
CREATE TABLE IF NOT EXISTS work_info (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT,
    zipcode TEXT,
    address TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_rent_info_zipcode ON rent_info(zipcode);
CREATE INDEX IF NOT EXISTS idx_work_info_zipcode ON work_info(zipcode);
CREATE INDEX IF NOT EXISTS idx_rent_info_created_at ON rent_info(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_work_info_created_at ON work_info(created_at DESC);
`;

async function createTables() {
  try {
    console.log('Creating database tables...');
    
    // 执行 SQL 创建表
    const { error } = await supabase.rpc('exec_sql', { sql: createTablesSQL });
    
    if (error) {
      console.error('Error creating tables:', error);
      
      // 如果 RPC 方法不存在，尝试直接执行
      console.log('Trying alternative method...');
      
      // 分别创建每个表
      const tables = [
        `CREATE TABLE IF NOT EXISTS users (
          id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
          username TEXT UNIQUE NOT NULL,
          email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          is_member BOOLEAN DEFAULT FALSE,
          membership_expires TIMESTAMP WITH TIME ZONE
        )`,
        `CREATE TABLE IF NOT EXISTS payments (
          id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
          user_id UUID REFERENCES users(id) ON DELETE CASCADE,
          amount DECIMAL(10,2) NOT NULL,
          payment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
          transaction_id TEXT UNIQUE
        )`,
        `CREATE TABLE IF NOT EXISTS rent_info (
          id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
          zipcode TEXT NOT NULL,
          address TEXT,
          content TEXT NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )`,
        `CREATE TABLE IF NOT EXISTS work_info (
          id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
          name TEXT,
          zipcode TEXT,
          address TEXT,
          content TEXT NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )`
      ];
      
      for (const sql of tables) {
        const { error: tableError } = await supabase.rpc('exec_sql', { sql });
        if (tableError) {
          console.error('Table creation error:', tableError);
        } else {
          console.log('✅ Table created successfully');
        }
      }
    } else {
      console.log('✅ All tables created successfully!');
    }
    
    // 验证表是否创建成功
    const { data: users, error: usersError } = await supabase
      .from('users')
      .select('count')
      .limit(1);
    
    if (usersError) {
      console.error('Users table still not accessible:', usersError);
    } else {
      console.log('✅ Users table is now accessible!');
    }
    
  } catch (error) {
    console.error('Create tables failed:', error);
  }
}

createTables(); 