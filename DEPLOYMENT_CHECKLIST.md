# 部署检查清单

## ✅ 支付功能已完成

### 1. 核心功能
- [x] 用户注册和登录系统
- [x] 会员权限管理
- [x] Stripe支付集成
- [x] Webhook处理
- [x] 支付记录存储
- [x] 会员过期时间管理

### 2. 安全功能
- [x] 密码加密存储
- [x] 用户会话管理
- [x] 会员权限验证装饰器
- [x] Webhook签名验证
- [x] 错误处理和日志记录

### 3. 前端界面
- [x] 会员购买页面
- [x] Stripe Elements集成
- [x] 支付状态反馈
- [x] 响应式设计

## 🔧 部署前配置

### 必需的环境变量

在服务器上设置以下环境变量：

```bash
# Flask应用配置
export SECRET_KEY="your-32-character-secret-key-here"
export FLASK_ENV="production"

# 数据库配置
export DATABASE_URL="sqlite:///instance/membership.db"
# 或者使用PostgreSQL: export DATABASE_URL="postgresql://user:password@host:port/dbname"

# Stripe配置
export STRIPE_SECRET_KEY="sk_live_your_stripe_secret_key"
export STRIPE_PUBLISHABLE_KEY="pk_live_your_stripe_publishable_key"
export STRIPE_WEBHOOK_SECRET="whsec_your_webhook_secret"
```

### Stripe账户设置

1. **创建Stripe账户**
   - 访问 [Stripe官网](https://stripe.com) 注册
   - 完成账户验证和激活

2. **获取API密钥**
   - 登录Stripe Dashboard
   - 进入 Developers → API Keys
   - 复制 Secret key 和 Publishable key

3. **配置Webhook**
   - 进入 Developers → Webhooks
   - 添加端点：`https://yourdomain.com/auth/stripe-webhook`
   - 选择事件：
     - `payment_intent.succeeded`
     - `payment_intent.payment_failed`
   - 复制Webhook签名密钥

4. **测试支付**
   - 使用测试卡号：`4242 4242 4242 4242`
   - 任意未来日期和CVC

## 🚀 部署步骤

### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和依赖
sudo apt install python3 python3-pip python3-venv nginx -y
```

### 2. 项目部署
```bash
# 克隆项目
git clone <your-repository-url>
cd newImmi

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境变量配置
```bash
# 创建.env文件
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/membership.db
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
FLASK_ENV=production
EOF
```

### 4. 运行应用
```bash
# 使用Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# 或者使用Systemd服务
sudo systemctl start newimmi
```

### 5. Nginx配置
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/newImmi/app/static;
    }
}
```

### 6. SSL证书
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

## 🧪 测试验证

### 1. 运行测试脚本
```bash
python test_payment.py
```

### 2. 功能测试
- [ ] 用户注册
- [ ] 用户登录
- [ ] 会员购买页面访问
- [ ] Stripe支付流程
- [ ] 会员权限验证
- [ ] Webhook处理

### 3. 安全测试
- [ ] 未登录用户无法访问会员功能
- [ ] 非会员用户无法访问付费功能
- [ ] Webhook签名验证
- [ ] 支付状态验证

## 📊 监控和维护

### 1. 日志监控
```bash
# 应用日志
sudo journalctl -u newimmi -f

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. 数据库备份
```bash
# SQLite备份
cp instance/membership.db instance/membership_backup_$(date +%Y%m%d).db

# PostgreSQL备份
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 3. 定期维护
- [ ] 更新依赖包
- [ ] 检查Stripe Dashboard
- [ ] 监控支付成功率
- [ ] 备份数据库
- [ ] 检查日志错误

## 🆘 故障排除

### 常见问题

1. **支付失败**
   - 检查Stripe API密钥
   - 确认账户已激活
   - 验证支付方式支持

2. **Webhook验证失败**
   - 检查Webhook密钥
   - 确认端点URL可访问
   - 验证事件类型

3. **会员权限问题**
   - 检查数据库连接
   - 验证会员过期时间
   - 确认用户状态

4. **静态文件404**
   - 检查Nginx配置
   - 确认文件权限
   - 验证文件路径

### 联系支持
- Stripe支持：https://support.stripe.com
- 应用日志：`sudo journalctl -u newimmi -f`
- 系统状态：`sudo systemctl status newimmi`

## 📝 部署完成确认

部署完成后，请确认以下功能正常工作：

- [ ] 网站可以正常访问
- [ ] 用户注册和登录功能
- [ ] 会员购买流程
- [ ] Stripe支付处理
- [ ] 会员权限验证
- [ ] Webhook回调处理
- [ ] 数据库记录正确
- [ ] SSL证书有效
- [ ] 错误日志正常

如果所有项目都检查通过，恭喜！您的支付系统已经成功部署并可以开始接受用户付费了。 