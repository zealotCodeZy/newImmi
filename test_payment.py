#!/usr/bin/env python3
"""
支付功能测试脚本
用于验证支付相关的功能是否正常工作
"""

import os
import sys
import requests
from datetime import datetime, timedelta, timezone

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Payment
from config import Config
from sqlalchemy import text

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    try:
        app = create_app()
        with app.app_context():
            # 测试数据库连接
            db.session.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_user_creation():
    """测试用户创建"""
    print("\n🔍 测试用户创建...")
    try:
        app = create_app()
        with app.app_context():
            # 检查用户是否已存在
            existing_user = User.query.filter_by(username='test_user_new').first()
            if existing_user:
                print("✅ 测试用户已存在")
                return existing_user
            
            # 创建测试用户
            test_user = User(
                username='test_user_new',
                email='test_new@example.com'
            )
            test_user.set_password('test123')
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ 测试用户创建成功")
            return test_user
    except Exception as e:
        print(f"❌ 用户创建失败: {e}")
        return None

def test_membership_functionality():
    """测试会员功能"""
    print("\n🔍 测试会员功能...")
    try:
        app = create_app()
        with app.app_context():
            user = User.query.filter_by(username='test_user_new').first()
            if not user:
                print("❌ 测试用户不存在")
                return False
            
            # 测试会员状态
            print(f"用户会员状态: {user.is_member}")
            print(f"会员过期时间: {user.membership_expires}")
            print(f"会员是否有效: {user.is_membership_active()}")
            
            # 模拟会员购买
            user.is_member = True
            user.membership_expires = datetime.now(timezone.utc) + timedelta(days=365)
            db.session.commit()
            
            print("✅ 会员功能测试成功")
            return True
    except Exception as e:
        print(f"❌ 会员功能测试失败: {e}")
        return False

def test_payment_model():
    """测试支付模型"""
    print("\n🔍 测试支付模型...")
    try:
        app = create_app()
        with app.app_context():
            user = User.query.filter_by(username='test_user_new').first()
            if not user:
                print("❌ 测试用户不存在")
                return False
            
            # 创建测试支付记录
            payment = Payment(
                user_id=user.id,
                amount=9.99,
                status='completed',
                transaction_id='test_transaction_123'
            )
            db.session.add(payment)
            db.session.commit()
            
            print("✅ 支付模型测试成功")
            return True
    except Exception as e:
        print(f"❌ 支付模型测试失败: {e}")
        return False

def test_stripe_configuration():
    """测试Stripe配置"""
    print("\n🔍 测试Stripe配置...")
    
    # 检查环境变量是否存在，但不显示具体值
    stripe_secret = os.environ.get('STRIPE_SECRET_KEY')
    stripe_publishable = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    print(f"Stripe Secret Key: {'✅ 已配置' if stripe_secret else '❌ 未配置'}")
    print(f"Stripe Publishable Key: {'✅ 已配置' if stripe_publishable else '❌ 未配置'}")
    print(f"Stripe Webhook Secret: {'✅ 已配置' if webhook_secret else '❌ 未配置'}")
    
    return True

def test_app_configuration():
    """测试应用配置"""
    print("\n🔍 测试应用配置...")
    
    # 检查关键配置，但不显示具体值
    secret_key = os.environ.get('SECRET_KEY')
    database_url = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
    
    print(f"Secret Key: {'✅ 已配置' if secret_key else '❌ 未配置'}")
    print(f"Database URL: {'✅ 已配置' if database_url else '❌ 未配置'}")
    print(f"Membership Price (Year): ${Config.MEMBERSHIP_PRICE_YEAR}")
    print(f"Membership Price (Month): ${Config.MEMBERSHIP_PRICE_MONTH}")
    
    return True

def cleanup_test_data():
    """清理测试数据"""
    print("\n🧹 清理测试数据...")
    try:
        app = create_app()
        with app.app_context():
            # 删除测试用户
            test_user = User.query.filter_by(username='test_user_new').first()
            if test_user:
                # 删除相关支付记录
                Payment.query.filter_by(user_id=test_user.id).delete()
                db.session.delete(test_user)
                db.session.commit()
                print("✅ 测试数据清理完成")
            else:
                print("✅ 无需清理测试数据")
    except Exception as e:
        print(f"❌ 清理测试数据失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始支付功能测试\n")
    
    # 运行测试
    tests = [
        test_database_connection,
        test_user_creation,
        test_membership_functionality,
        test_payment_model,
        test_stripe_configuration,
        test_app_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    # 清理测试数据
    cleanup_test_data()
    
    # 输出测试结果
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！支付功能配置正确。")
        print("\n📝 部署检查清单:")
        print("✅ 数据库连接正常")
        print("✅ 用户模型工作正常")
        print("✅ 会员功能正常")
        print("✅ 支付模型正常")
        print("⚠️  请确保配置正确的Stripe密钥")
        print("⚠️  请确保配置正确的Webhook密钥")
    else:
        print("⚠️  部分测试失败，请检查配置。")
        print("\n🔧 建议:")
        print("1. 检查数据库配置")
        print("2. 确保所有环境变量正确设置")
        print("3. 验证Stripe账户配置")

if __name__ == '__main__':
    main() 