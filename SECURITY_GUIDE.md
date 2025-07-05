# 安全配置指南

## 🚨 重要安全提醒

### 1. 环境变量管理

**✅ 正确做法：**
```bash
# 在服务器上设置环境变量
export SECRET_KEY="your-actual-secret-key"
export STRIPE_SECRET_KEY="sk_live_your_actual_key"
export STRIPE_PUBLISHABLE_KEY="pk_live_your_actual_key"
export STRIPE_WEBHOOK_SECRET="whsec_your_actual_webhook_secret"
```

**❌ 错误做法：**
```python
# 永远不要在代码中硬编码密钥
SECRET_KEY = "hardcoded-secret-key"
STRIPE_SECRET_KEY = "sk_live_hardcoded_key"
```

### 2. 文件保护

**✅ 已配置的保护：**
- `.env` 文件已添加到 `.gitignore`
- 数据库文件已添加到 `.gitignore`
- 敏感配置文件已添加到 `.gitignore`

**🔒 额外保护措施：**
```bash
# 设置文件权限
chmod 600 .env
chmod 600 instance/*.db

# 确保只有应用用户可以访问
chown www-data:www-data .env
chown www-data:www-data instance/
```

### 3. 日志安全

**✅ 当前代码已安全：**
- 日志中不包含密钥信息
- 只记录操作状态和用户ID
- 错误信息不泄露敏感数据

**🔍 日志示例：**
```python
# ✅ 安全的日志
logger.info(f"用户 {username} 成功购买会员")
logger.error(f"支付处理失败: {error_type}")

# ❌ 不安全的日志（已避免）
logger.info(f"使用密钥: {stripe_secret_key}")
```

## 🔧 安全配置步骤

### 1. 生成安全的SECRET_KEY

```bash
# 方法1：使用Python
python -c "import secrets; print(secrets.token_hex(32))"

# 方法2：使用OpenSSL
openssl rand -hex 32

# 方法3：使用在线工具（仅用于测试）
# 访问 https://generate-secret.vercel.app/32
```

### 2. 配置Stripe密钥

1. **登录Stripe Dashboard**
   - 访问 https://dashboard.stripe.com
   - 完成账户验证

2. **获取API密钥**
   - Developers → API Keys
   - 复制 Secret key 和 Publishable key

3. **配置Webhook**
   - Developers → Webhooks
   - 添加端点：`https://yourdomain.com/auth/stripe-webhook`
   - 选择事件：`payment_intent.succeeded`, `payment_intent.payment_failed`
   - 复制Webhook签名密钥

### 3. 环境变量设置

**开发环境：**
```bash
# 创建.env文件
cat > .env << EOF
SECRET_KEY=your-generated-secret-key
DATABASE_URL=sqlite:///instance/membership.db
STRIPE_SECRET_KEY=sk_test_your_test_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_key
STRIPE_WEBHOOK_SECRET=whsec_your_test_webhook_secret
FLASK_ENV=development
EOF
```

**生产环境：**
```bash
# 在服务器上设置
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgresql://user:password@host:port/dbname"
export STRIPE_SECRET_KEY="sk_live_your_production_key"
export STRIPE_PUBLISHABLE_KEY="pk_live_your_production_key"
export STRIPE_WEBHOOK_SECRET="whsec_your_production_webhook_secret"
export FLASK_ENV="production"
```

## 🛡️ 安全最佳实践

### 1. 密钥轮换

**定期轮换密钥：**
```bash
# 生成新的SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# 在Stripe Dashboard中轮换API密钥
# 1. 生成新的API密钥
# 2. 更新环境变量
# 3. 测试新密钥
# 4. 删除旧密钥
```

### 2. 访问控制

**文件权限：**
```bash
# 设置正确的文件权限
chmod 600 .env
chmod 644 *.py
chmod 755 app/
chmod 755 templates/
```

**用户权限：**
```bash
# 使用专用用户运行应用
sudo useradd -r -s /bin/false newimmi
sudo chown -R newimmi:newimmi /path/to/newImmi
```

### 3. 网络安全

**防火墙配置：**
```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

**SSL证书：**
```bash
# 强制HTTPS
sudo certbot --nginx -d yourdomain.com
```

### 4. 监控和审计

**日志监控：**
```bash
# 监控应用日志
sudo journalctl -u newimmi -f

# 监控访问日志
sudo tail -f /var/log/nginx/access.log

# 监控错误日志
sudo tail -f /var/log/nginx/error.log
```

**安全扫描：**
```bash
# 定期检查依赖包安全漏洞
pip-audit

# 检查系统安全更新
sudo apt update && sudo apt upgrade
```

## 🚨 安全检查清单

部署前请确认：

- [ ] 所有密钥都通过环境变量配置
- [ ] 没有硬编码的密钥在代码中
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 文件权限设置正确
- [ ] 使用HTTPS
- [ ] 防火墙配置正确
- [ ] 定期备份数据库
- [ ] 监控日志文件
- [ ] 定期更新依赖包
- [ ] 测试环境使用测试密钥
- [ ] 生产环境使用生产密钥

## 🔍 安全测试

运行安全测试：
```bash
# 运行支付功能测试
python test_payment.py

# 检查是否有硬编码密钥
grep -r "sk_test\|sk_live\|pk_test\|pk_live\|whsec_" . --exclude-dir=venv --exclude-dir=lib

# 检查文件权限
ls -la .env
ls -la instance/
```

## 📞 安全事件响应

如果发现安全事件：

1. **立即隔离**：停止应用服务
2. **评估影响**：确定泄露的范围
3. **轮换密钥**：立即更换所有密钥
4. **通知用户**：如果用户数据受影响
5. **修复漏洞**：解决根本原因
6. **恢复服务**：使用新密钥重新部署
7. **监控异常**：密切监控系统活动

## 📚 安全资源

- [OWASP安全指南](https://owasp.org/www-project-top-ten/)
- [Stripe安全最佳实践](https://stripe.com/docs/security)
- [Flask安全文档](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python安全指南](https://python-security.readthedocs.io/) 