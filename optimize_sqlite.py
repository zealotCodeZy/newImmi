#!/usr/bin/env python3
"""
SQLite生产环境优化脚本
用于配置SQLite数据库以提高性能和并发能力
"""

import sqlite3
import os
from pathlib import Path

def optimize_sqlite_database():
    """优化SQLite数据库配置"""
    print("🔧 开始优化SQLite数据库...")
    
    # 获取数据库路径
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'membership.db')
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        print("请先运行应用创建数据库")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ 连接到数据库: {db_path}")
        
        # 1. 启用WAL模式（Write-Ahead Logging）
        print("📝 启用WAL模式...")
        cursor.execute("PRAGMA journal_mode=WAL")
        result = cursor.fetchone()
        print(f"   日志模式: {result[0]}")
        
        # 2. 设置同步模式
        print("⚡ 优化同步模式...")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA synchronous")
        result = cursor.fetchone()
        print(f"   同步模式: {result[0]}")
        
        # 3. 设置缓存大小
        print("💾 优化缓存大小...")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA cache_size")
        result = cursor.fetchone()
        print(f"   缓存大小: {result[0]} 页")
        
        # 4. 设置临时存储
        print("📁 配置临时存储...")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA temp_store")
        result = cursor.fetchone()
        print(f"   临时存储: {result[0]}")
        
        # 5. 设置页面大小
        print("📄 优化页面大小...")
        cursor.execute("PRAGMA page_size=4096")
        cursor.execute("PRAGMA page_size")
        result = cursor.fetchone()
        print(f"   页面大小: {result[0]} 字节")
        
        # 6. 启用外键约束
        print("🔗 启用外键约束...")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA foreign_keys")
        result = cursor.fetchone()
        print(f"   外键约束: {'启用' if result[0] else '禁用'}")
        
        # 7. 分析表结构
        print("📊 分析表结构...")
        cursor.execute("ANALYZE")
        print("   表分析完成")
        
        # 8. 获取数据库信息
        print("📈 数据库统计信息:")
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"   用户数量: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM payment")
        payment_count = cursor.fetchone()[0]
        print(f"   支付记录: {payment_count}")
        
        # 9. 检查WAL文件
        wal_path = db_path + '-wal'
        if os.path.exists(wal_path):
            wal_size = os.path.getsize(wal_path)
            print(f"   WAL文件大小: {wal_size} 字节")
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print("✅ SQLite数据库优化完成！")
        return True
        
    except Exception as e:
        print(f"❌ 优化失败: {e}")
        return False

def create_backup():
    """创建数据库备份"""
    print("\n💾 创建数据库备份...")
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'membership.db')
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False
    
    try:
        import shutil
        from datetime import datetime
        
        # 创建备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(basedir, 'instance', f'membership_backup_{timestamp}.db')
        
        # 复制数据库文件
        shutil.copy2(db_path, backup_path)
        
        # 获取文件大小
        size = os.path.getsize(backup_path)
        print(f"✅ 备份创建成功: {backup_path}")
        print(f"   备份大小: {size} 字节")
        
        return True
        
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return False

def check_performance():
    """检查数据库性能"""
    print("\n🚀 检查数据库性能...")
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'membership.db')
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 测试查询性能
        import time
        
        # 测试用户查询
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        user_time = time.time() - start_time
        
        # 测试支付查询
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM payment")
        payment_count = cursor.fetchone()[0]
        payment_time = time.time() - start_time
        
        # 测试复杂查询
        start_time = time.time()
        cursor.execute("""
            SELECT u.username, p.amount, p.payment_date 
            FROM user u 
            JOIN payment p ON u.id = p.user_id 
            ORDER BY p.payment_date DESC 
            LIMIT 10
        """)
        complex_result = cursor.fetchall()
        complex_time = time.time() - start_time
        
        conn.close()
        
        print(f"✅ 性能测试结果:")
        print(f"   用户查询: {user_count} 条记录, {user_time:.4f} 秒")
        print(f"   支付查询: {payment_count} 条记录, {payment_time:.4f} 秒")
        print(f"   复杂查询: {len(complex_result)} 条记录, {complex_time:.4f} 秒")
        
        # 性能评估
        if user_time < 0.01 and payment_time < 0.01 and complex_time < 0.05:
            print("🎉 性能优秀！")
        elif user_time < 0.1 and payment_time < 0.1 and complex_time < 0.5:
            print("✅ 性能良好")
        else:
            print("⚠️  性能可能需要优化")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 SQLite生产环境优化工具\n")
    
    # 检查数据库是否存在
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'membership.db')
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在，请先运行应用创建数据库")
        print("运行命令: python main.py")
        return
    
    # 执行优化
    if optimize_sqlite_database():
        # 创建备份
        create_backup()
        
        # 检查性能
        check_performance()
        
        print("\n📝 优化建议:")
        print("✅ 定期备份数据库文件")
        print("✅ 监控WAL文件大小")
        print("✅ 定期运行VACUUM命令清理空间")
        print("✅ 如果数据量增长到10000+条，考虑迁移到PostgreSQL")
        
    else:
        print("❌ 优化失败")

if __name__ == '__main__':
    main() 