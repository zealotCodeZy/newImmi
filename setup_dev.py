#!/usr/bin/env python3
"""
开发环境设置脚本
用于快速配置开发环境的环境变量
"""

import os
import secrets

def setup_dev_environment():
    """设置开发环境"""
    print("🔧 设置开发环境...")
    
    # 生成开发用的SECRET_KEY
    secret_key = secrets.token_hex(32)
    
    # 设置环境变量
    os.environ['SECRET_KEY'] = secret_key
    os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STQ901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
    os.environ['DATABASE_URL'] = 'sqlite:///instance/membership.db'
    os.environ['FLASK_ENV'] = 'development'
    
    print("✅ 开发环境变量设置完成")
    print(f"   SECRET_KEY: {secret_key[:10]}...")
    print("   STRIPE_SECRET_KEY: sk_test_...")
    print("   STRIPE_PUBLISHABLE_KEY: pk_test_...")
    print("   STRIPE_WEBHOOK_SECRET: whsec_...")
    print("   DATABASE_URL: sqlite:///instance/membership.db")
    
    return True

if __name__ == '__main__':
    setup_dev_environment() 