# NewImmi 项目部署指南

## 项目架构

- **前端**: Vercel 静态站点 (`static_site/`)
- **后端**: Vercel Serverless Functions (`api-vercel/`)
- **数据库**: Supabase PostgreSQL
- **认证**: JWT + Supabase Auth
- **支付**: Stripe

## 部署步骤

### 1. 设置 Supabase 数据库

1. 登录 [Supabase](https://supabase.com)
2. 创建新项目
3. 获取项目 URL 和 Service Role Key
4. 运行数据库迁移：

```bash
cd api-vercel
supabase db push
```

### 2. 设置环境变量

在 Vercel 项目设置中添加以下环境变量：

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

### 3. 部署后端 API

```bash
cd api-vercel
vercel --prod
```

### 4. 更新前端 API 端点

在 `static_site/` 目录中，更新所有 API 调用为新的 Vercel 端点：

```javascript
// 旧端点
const API_BASE = 'https://your-render-app.onrender.com';

// 新端点
const API_BASE = 'https://your-vercel-app.vercel.app/api';
```

### 5. 部署前端

```bash
cd static_site
vercel --prod
```

### 6. 设置 Stripe Webhook

1. 在 Stripe Dashboard 中创建 Webhook
2. 端点 URL: `https://your-vercel-app.vercel.app/api/stripe/webhook`
3. 选择事件：
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`

## 本地开发

### 后端开发

```bash
cd api-vercel
npm install
cp env.example .env.local
# 编辑 .env.local 文件
npm run dev
```

### 前端开发

```bash
cd static_site
# 使用 Live Server 或其他静态文件服务器
```

## 数据库迁移

如果需要修改数据库结构：

1. 创建新的迁移文件：
```bash
cd api-vercel
supabase migration new migration_name
```

2. 编辑生成的 SQL 文件

3. 应用迁移：
```bash
supabase db push
```

## 故障排除

### 常见问题

1. **CORS 错误**: 确保 Vercel 配置中的 CORS 头设置正确
2. **环境变量未找到**: 检查 Vercel 项目设置中的环境变量
3. **数据库连接失败**: 验证 Supabase URL 和 Service Role Key
4. **Stripe Webhook 失败**: 检查 Webhook 端点 URL 和签名验证

### 日志查看

- Vercel 函数日志: Vercel Dashboard > Functions
- Supabase 日志: Supabase Dashboard > Logs
- Stripe 日志: Stripe Dashboard > Webhooks

## 性能优化

1. **数据库索引**: 确保查询字段有适当的索引
2. **缓存策略**: 考虑使用 Redis 或 Vercel Edge Cache
3. **CDN**: 静态资源通过 Vercel CDN 分发
4. **函数优化**: 减少冷启动时间，优化依赖包大小

## 安全考虑

1. **环境变量**: 不要在代码中硬编码敏感信息
2. **API 密钥轮换**: 定期更新 API 密钥
3. **输入验证**: 所有用户输入都要验证
4. **SQL 注入防护**: 使用参数化查询
5. **CORS 配置**: 限制允许的域名 