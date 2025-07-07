#!/usr/bin/env python3
"""
简化的开发环境启动脚本
使用简化的SQLite配置避免连接问题
"""

import os
import secrets
import subprocess
import sys

def setup_dev_environment():
    """设置开发环境变量"""
    print("🔧 设置开发环境变量...")
    
    # 生成开发用的SECRET_KEY
    secret_key = secrets.token_hex(32)
    
    # 设置环境变量
    os.environ['SECRET_KEY'] = secret_key
    os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STQ901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
    os.environ['FLASK_ENV'] = 'development'
    
    print("✅ 环境变量设置完成")
    print(f"   SECRET_KEY: {secret_key[:10]}...")
    print("   STRIPE_SECRET_KEY: sk_test_...")
    print("   STRIPE_PUBLISHABLE_KEY: pk_test_...")
    print("   STRIPE_WEBHOOK_SECRET: whsec_...")
    
    return True

def create_database_directory():
    """创建数据库目录"""
    print("🗄️  准备数据库目录...")
    try:
        os.makedirs('instance', exist_ok=True)
        # 确保数据库文件有正确的权限
        db_path = os.path.join('instance', 'membership.db')
        if os.path.exists(db_path):
            os.chmod(db_path, 0o644)
        print("✅ 数据库目录准备完成")
        return True
    except Exception as e:
        print(f"❌ 数据库目录创建失败: {e}")
        return False

def start_application():
    """启动应用"""
    print("🚀 启动 NewImmi 应用...")
    print("应用将在 http://localhost:5002 启动")
    print("按 Ctrl+C 停止应用")
    
    try:
        # 直接运行main.py
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")

def main():
    """主函数"""
    print("🚀 开始启动 NewImmi 开发环境...")
    
    # 设置环境变量
    if not setup_dev_environment():
        return
    
    # 创建数据库目录
    if not create_database_directory():
        return
    
    # 启动应用
    start_application()

if __name__ == '__main__':
    main() 