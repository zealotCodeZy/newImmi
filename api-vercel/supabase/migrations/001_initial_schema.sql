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

-- 启用 Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE rent_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE work_info ENABLE ROW LEVEL SECURITY;

-- 创建 RLS 策略
-- 用户只能查看自己的信息
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

-- 用户只能更新自己的信息
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 支付记录只能由用户自己查看
CREATE POLICY "Users can view own payments" ON payments
    FOR SELECT USING (auth.uid()::text = user_id::text);

-- 租房信息所有人可读，登录用户可写
CREATE POLICY "Anyone can read rent info" ON rent_info
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert rent info" ON rent_info
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- 工作信息所有人可读，登录用户可写
CREATE POLICY "Anyone can read work info" ON work_info
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert work info" ON work_info
    FOR INSERT WITH CHECK (auth.role() = 'authenticated'); 