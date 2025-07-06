#!/usr/bin/env python3
"""
数据库连接测试脚本
"""

import os
import sqlite3
import secrets

def test_sqlite_connection():
    """测试SQLite连接"""
    print("🔧 测试SQLite数据库连接...")
    
    # 设置环境变量
    secret_key = secrets.token_hex(32)
    os.environ['SECRET_KEY'] = secret_key
    os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51ABC123DEF456GHI789JKL012MNO345PQR678STQ901VWX234YZA567BCD890EFG'
    os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
    os.environ['DATABASE_URL'] = 'sqlite:///instance/membership.db'
    os.environ['FLASK_ENV'] = 'development'
    
    # 确保instance目录存在
    os.makedirs('instance', exist_ok=True)
    
    # 测试直接SQLite连接
    db_path = os.path.join('instance', 'membership.db')
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ SQLite连接成功: {db_path}")
        
        # 创建测试表
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()
        print("✅ 测试表创建成功")
        
        # 插入测试数据
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        conn.commit()
        print("✅ 测试数据插入成功")
        
        # 查询测试数据
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchall()
        print(f"✅ 查询结果: {result}")
        
        conn.close()
        print("✅ SQLite测试完成")
        return True
        
    except Exception as e:
        print(f"❌ SQLite连接失败: {e}")
        return False

def test_flask_sqlalchemy():
    """测试Flask-SQLAlchemy连接"""
    print("\n🔧 测试Flask-SQLAlchemy连接...")
    
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # 测试数据库连接
            db.engine.execute("SELECT 1")
            print("✅ Flask-SQLAlchemy连接成功")
            
            # 测试模型
            print("✅ 模型导入成功")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask-SQLAlchemy测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始数据库连接测试...")
    
    # 测试SQLite连接
    if not test_sqlite_connection():
        return
    
    # 测试Flask-SQLAlchemy
    if not test_flask_sqlalchemy():
        return
    
    print("\n🎉 所有测试通过！数据库连接正常")

if __name__ == '__main__':
    main() 