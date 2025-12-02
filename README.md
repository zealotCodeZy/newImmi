# 新移民防踩坑 - NewImmi

为新移民提供租房、工作信息查询和黑名单预警的会员制服务平台。

## 🌟 功能特性

### 核心功能
- 🏠 **租房信息查询** - 查询租房信息和黑名单预警
- 💼 **工作信息查询** - 查找工作机会和雇主评价
- 🏦 **银行开户指南** - 新移民银行开户攻略
- 📱 **手机办理指南** - 手机套餐和运营商对比
- 🪪 **证件办理指南** - 驾照、ID 等证件办理流程

### 用户系统
- 🔐 用户注册和登录（JWT 认证）
- 💎 会员订阅系统（Stripe 支付）
- 👤 个人信息管理
- 🔒 会员权限控制

## 🏗️ 技术架构

### 前端
- **框架**: 静态 HTML/CSS/JavaScript
- **部署**: Vercel Static Hosting
- **特性**: 响应式设计、轮播图、动态内容加载

### 后端 API
- **平台**: Vercel Serverless Functions
- **语言**: TypeScript/Node.js
- **认证**: JWT Token
- **支付**: Stripe Integration

### 数据库
- **服务**: Supabase PostgreSQL
- **特性**: 实时数据、Row Level Security
- **备份**: 自动备份

## 📁 项目结构

```
newImmi/
├── api-vercel/              # 后端 API (Vercel Serverless)
│   ├── api/                 # API 路由
│   │   ├── auth/           # 认证相关
│   │   ├── rent/           # 租房信息
│   │   ├── work/           # 工作信息
│   │   ├── membership/     # 会员管理
│   │   └── stripe/         # Stripe 支付
│   ├── lib/                # 工具库
│   └── vercel.json         # Vercel 配置
│
├── static_site/            # 前端静态站点
│   ├── *.html             # 页面文件
│   ├── static/            # 静态资源
│   │   ├── css/          # 样式文件
│   │   ├── js/           # JavaScript
│   │   └── images/       # 图片资源
│   └── vercel.json        # Vercel 配置
│
├── supabase/              # Supabase 配置
├── DEPLOYMENT_GUIDE.md    # 部署指南
└── README.md              # 项目说明
```

## 🚀 快速开始

### 本地开发

#### 后端 API
```bash
cd api-vercel
npm install
cp env.example .env.local
# 编辑 .env.local 配置环境变量
npm run dev
```

#### 前端站点
```bash
cd static_site
# 使用任意静态服务器，如 Live Server
```

### 部署到 Vercel

#### 1. 部署后端 API
```bash
cd api-vercel
vercel --prod
```

#### 2. 部署前端站点
```bash
cd static_site
vercel --prod
```

详细部署步骤请参考 [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

## 🔧 环境变量配置

在 Vercel 项目设置中配置以下环境变量：

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# JWT
JWT_SECRET=your_jwt_secret

# Stripe
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

## 📊 数据库表结构

### users
- 用户基本信息
- 会员状态和过期时间
- 密码哈希存储

### payments
- 支付记录
- Stripe 交易 ID
- 支付状态追踪

### rent_info
- 租房信息
- 地址和邮编
- 用户评价内容

### work_info
- 工作信息
- 公司名称和地址
- 雇主评价

## 🔐 安全特性

- JWT Token 认证
- 密码 bcrypt 加密
- Supabase Row Level Security
- CORS 跨域保护
- Stripe Webhook 签名验证

## 📝 开发指南

### API 端点

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/rent` - 获取租房信息（需会员）
- `GET /api/work` - 获取工作信息（需会员）
- `POST /api/membership` - 创建会员订阅
- `POST /api/stripe/webhook` - Stripe Webhook

### 前端页面

- `index.html` - 首页
- `rent.html` / `rentBlack.html` - 租房查询
- `work.html` / `workBlack.html` - 工作查询
- `membership.html` - 会员购买
- `login.html` / `register.html` - 登录注册

## 🌐 在线访问

- **前端**: https://your-site.vercel.app
- **API**: https://your-api.vercel.app

## 📄 许可证

Copyright ©2025 新移民第一站 All Rights Reserved 