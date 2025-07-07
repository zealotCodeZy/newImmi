#!/usr/bin/env python3
"""
数据输入脚本
用于快速添加测试数据到数据库
"""

import os
import sys
from datetime import datetime, timedelta
import secrets

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置开发环境变量
os.environ['SECRET_KEY'] = secrets.token_hex(32)
os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZA567BCD890EFG'
os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STQ901VWX234YZA567BCD890EFG'
os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models import User, Payment

def add_sample_users():
    """添加示例用户"""
    print("👥 添加示例用户...")
    
    sample_users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'is_member': True
        },
        {
            'username': 'testuser1',
            'email': 'user1@example.com',
            'password': 'password123',
            'is_member': True
        },
        {
            'username': 'testuser2',
            'email': 'user2@example.com',
            'password': 'password123',
            'is_member': False
        },
        {
            'username': 'vipuser',
            'email': 'vip@example.com',
            'password': 'vip123',
            'is_member': True
        }
    ]
    
    app = create_app()
    with app.app_context():
        for user_data in sample_users:
            # 检查用户是否已存在
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if existing_user:
                print(f"   ⚠️  用户 {user_data['username']} 已存在，跳过")
                continue
            
            # 创建用户
            user = User()
            user.username = user_data['username']
            user.email = user_data['email']
            user.set_password(user_data['password'])
            user.is_member = user_data['is_member']
            
            if user_data['is_member']:
                user.membership_expires = datetime.now() + timedelta(days=365)
            
            db.session.add(user)
            print(f"   ✅ 添加用户: {user_data['username']}")
        
        db.session.commit()
        print("✅ 示例用户添加完成")

def add_sample_payments():
    """添加示例支付记录"""
    print("\n💰 添加示例支付记录...")
    
    app = create_app()
    with app.app_context():
        # 获取所有用户
        users = User.query.all()
        
        if not users:
            print("   ⚠️  没有用户，无法添加支付记录")
            return
        
        sample_payments = [
            {'user_id': 1, 'amount': 9.99, 'status': 'completed'},
            {'user_id': 1, 'amount': 0.99, 'status': 'completed'},
            {'user_id': 2, 'amount': 9.99, 'status': 'completed'},
            {'user_id': 4, 'amount': 9.99, 'status': 'completed'},
        ]
        
        for payment_data in sample_payments:
            # 检查用户是否存在
            user = User.query.get(payment_data['user_id'])
            if not user:
                print(f"   ⚠️  用户ID {payment_data['user_id']} 不存在，跳过")
                continue
            
            # 创建支付记录
            payment = Payment()
            payment.user_id = payment_data['user_id']
            payment.amount = payment_data['amount']
            payment.status = payment_data['status']
            payment.transaction_id = f'sample_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{payment_data["user_id"]}'
            
            db.session.add(payment)
            print(f"   ✅ 添加支付记录: 用户 {user.username}, 金额 ${payment_data['amount']}")
        
        db.session.commit()
        print("✅ 示例支付记录添加完成")

def interactive_add_user():
    """交互式添加用户"""
    print("\n👤 交互式添加用户")
    print("输入 'quit' 退出")
    
    app = create_app()
    with app.app_context():
        while True:
            print("\n" + "="*50)
            
            username = input("用户名: ").strip()
            if username.lower() == 'quit':
                break
            
            if not username:
                print("❌ 用户名不能为空")
                continue
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                print("❌ 用户名已存在")
                continue
            
            email = input("邮箱: ").strip()
            if not email:
                print("❌ 邮箱不能为空")
                continue
            
            # 检查邮箱是否已存在
            if User.query.filter_by(email=email).first():
                print("❌ 邮箱已被注册")
                continue
            
            password = input("密码: ").strip()
            if not password:
                print("❌ 密码不能为空")
                continue
            
            is_member = input("是否会员 (y/n): ").strip().lower() == 'y'
            
            # 创建用户
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.is_member = is_member
            
            if is_member:
                user.membership_expires = datetime.now() + timedelta(days=365)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ 用户 {username} 添加成功")

def show_database_stats():
    """显示数据库统计信息"""
    print("\n📊 数据库统计信息")
    
    app = create_app()
    with app.app_context():
        total_users = User.query.count()
        total_payments = Payment.query.count()
        active_members = User.query.filter_by(is_member=True).count()
        
        print(f"   总用户数: {total_users}")
        print(f"   总支付记录: {total_payments}")
        print(f"   活跃会员: {active_members}")
        
        # 显示最近注册的用户
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        if recent_users:
            print("\n   最近注册的用户:")
            for user in recent_users:
                print(f"     - {user.username} ({user.email}) - {'会员' if user.is_member else '普通用户'}")

def main():
    """主函数"""
    print("📝 数据输入工具")
    print("="*50)
    
    while True:
        print("\n请选择操作:")
        print("1. 添加示例用户")
        print("2. 添加示例支付记录")
        print("3. 交互式添加用户")
        print("4. 显示数据库统计")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            add_sample_users()
        elif choice == '2':
            add_sample_payments()
        elif choice == '3':
            interactive_add_user()
        elif choice == '4':
            show_database_stats()
        elif choice == '5':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == '__main__':
    main() 