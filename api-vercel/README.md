# NewImmi API - Vercel Serverless Functions

基于 Vercel Serverless Functions + Supabase 的新移民信息平台 API。

## 技术栈

- **API 层**: Vercel Serverless Functions (TypeScript)
- **数据库**: Supabase PostgreSQL
- **认证**: JWT + Supabase Auth
- **支付**: Stripe
- **前端**: Vercel 静态站点

## 项目结构

```
api-vercel/
├── api/                    # API 路由
│   ├── auth/              # 认证相关
│   │   ├── login.ts       # 用户登录
│   │   └── register.ts    # 用户注册
│   ├── rent/              # 租房信息
│   │   └── index.ts       # 租房 CRUD
│   ├── work/              # 工作信息
│   │   └── index.ts       # 工作 CRUD
│   └── stripe/            # Stripe 集成
│       └── webhook.ts     # Stripe Webhook
├── lib/                   # 工具库
│   ├── supabase.ts        # Supabase 客户端
│   └── utils.ts           # 通用工具函数
├── vercel.json            # Vercel 配置
├── tsconfig.json          # TypeScript 配置
└── package.json           # 依赖管理
```

## 环境变量

复制 `env.example` 为 `.env.local` 并填写以下变量：

```bash
# Supabase 配置
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# JWT 配置
JWT_SECRET=your_jwt_secret_key

# Stripe 配置
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

## 本地开发

1. 安装依赖：
```bash
npm install
```

2. 设置环境变量：
```bash
cp env.example .env.local
# 编辑 .env.local 文件
```

3. 本地运行：
```bash
vercel dev
```

## 部署

1. 部署到 Vercel：
```bash
vercel --prod
```

2. 设置环境变量：
在 Vercel 项目设置中添加环境变量。

## API 端点

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 租房信息
- `GET /api/rent` - 获取租房信息
- `POST /api/rent` - 创建租房信息

### 工作信息
- `GET /api/work` - 获取工作信息
- `POST /api/work` - 创建工作信息

### Stripe
- `POST /api/stripe/webhook` - Stripe Webhook 处理

## 数据库表结构

### users 表
- id (uuid, primary key)
- username (text, unique)
- email (text, unique)
- password_hash (text)
- created_at (timestamp)
- is_member (boolean)
- membership_expires (timestamp)

### payments 表
- id (uuid, primary key)
- user_id (uuid, foreign key)
- amount (decimal)
- payment_date (timestamp)
- status (text)
- transaction_id (text, unique)

### rent_info 表
- id (uuid, primary key)
- zipcode (text)
- address (text)
- content (text)
- created_at (timestamp)

### work_info 表
- id (uuid, primary key)
- name (text)
- zipcode (text)
- address (text)
- content (text)
- created_at (timestamp) 