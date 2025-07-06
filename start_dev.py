#!/usr/bin/env bash
# 一条命令直接配置环境变量并启动Flask应用，支持自定义端口

echo "🚀 开始启动 NewImmi 开发环境..."

# 生成随机SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# 你可以在这里自定义测试用的Stripe key
STRIPE_SECRET_KEY="sk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZA567BCD890EFG"
STRIPE_PUBLISHABLE_KEY="pk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STQ901VWX234YZA567BCD890EFG"
STRIPE_WEBHOOK_SECRET="whsec_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

# 用绝对路径
DATABASE_URL="sqlite:///${PWD}/instance/membership.db"
FLASK_ENV=development
PORT=${1:-5002}  # 默认5002端口，可通过第一个参数自定义

echo "🔧 设置环境变量..."
echo "   SECRET_KEY: ${SECRET_KEY:0:10}..."
echo "   DATABASE_URL: $DATABASE_URL"

# 确保instance目录存在
echo "🗄️  准备数据库目录..."
mkdir -p instance
chmod 755 instance

# 删除可能有问题的数据库文件
rm -f instance/membership.db

# 安装依赖（可选，已装可注释）
echo "📦 检查依赖..."
pip install -r requirements.txt > /dev/null 2>&1

# 启动Flask应用
echo "🚀 启动应用..."
export SECRET_KEY STRIPE_SECRET_KEY STRIPE_PUBLISHABLE_KEY STRIPE_WEBHOOK_SECRET DATABASE_URL FLASK_ENV

# 启动
python3 main.py 