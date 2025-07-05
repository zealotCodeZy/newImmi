#!/bin/bash

# 部署脚本示例
# 使用前请修改以下变量为你的实际值

echo "🚀 开始部署 NewImmi 应用..."

# 1. 检查必要的环境变量
echo "📋 检查环境变量..."

if [ -z "$SECRET_KEY" ]; then
    echo "❌ 错误: SECRET_KEY 环境变量未设置"
    echo "请运行: export SECRET_KEY='your-secret-key'"
    exit 1
fi

if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "❌ 错误: STRIPE_SECRET_KEY 环境变量未设置"
    echo "请运行: export STRIPE_SECRET_KEY='sk_live_your_key'"
    exit 1
fi

if [ -z "$STRIPE_PUBLISHABLE_KEY" ]; then
    echo "❌ 错误: STRIPE_PUBLISHABLE_KEY 环境变量未设置"
    echo "请运行: export STRIPE_PUBLISHABLE_KEY='pk_live_your_key'"
    exit 1
fi

if [ -z "$STRIPE_WEBHOOK_SECRET" ]; then
    echo "❌ 错误: STRIPE_WEBHOOK_SECRET 环境变量未设置"
    echo "请运行: export STRIPE_WEBHOOK_SECRET='whsec_your_webhook_secret'"
    exit 1
fi

echo "✅ 环境变量检查通过"

# 2. 验证配置
echo "🔧 验证应用配置..."
python -c "from config import Config; print('✅ 配置验证成功')" || {
    echo "❌ 配置验证失败"
    exit 1
}

# 3. 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 4. 创建数据库目录
echo "🗄️  准备数据库..."
mkdir -p instance
chmod 700 instance

# 5. 优化SQLite数据库（如果使用SQLite）
if [[ "$DATABASE_URL" == *"sqlite"* ]] || [[ -z "$DATABASE_URL" ]]; then
    echo "🔧 优化SQLite数据库..."
    python optimize_sqlite.py
fi

# 6. 运行安全测试
echo "🛡️  运行安全检查..."
python security_check.py

# 7. 运行功能测试
echo "🧪 运行功能测试..."
python test_payment.py

# 8. 启动应用
echo "🚀 启动应用..."
echo "应用将在 http://localhost:8000 启动"
echo "按 Ctrl+C 停止应用"

gunicorn -w 4 -b 0.0.0.0:8000 main:app 