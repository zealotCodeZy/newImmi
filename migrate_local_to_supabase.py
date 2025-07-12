#!/usr/bin/env python3
"""
从本地 PostgreSQL 迁移数据到 Supabase
"""

import os
import subprocess
import json
from datetime import datetime

# 本地 PostgreSQL 连接信息
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'newimmi_db',
    'user': 'newimmi_user',
    'password': ''  # 如果需要密码，请填写
}

# Supabase 连接信息
SUPABASE_URL = 'https://wbjbnfogbsiwqwnopocn.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndiamJuZm9nYnNpd3F3bm9wb2NuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjI0Njk2MywiZXhwIjoyMDY3ODIyOTYzfQ.qgo76VLXsnXKfpxeTyYA7t76QIlEpsC4b5jv8HdY5ro'

def run_command(cmd, description):
    """执行命令并处理错误"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} 成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def export_local_data():
    """从本地 PostgreSQL 导出数据"""
    # 构建 pg_dump 命令
    password_part = f"PGPASSWORD={LOCAL_DB_CONFIG['password']}" if LOCAL_DB_CONFIG['password'] else ""
    
    cmd = f"{password_part} pg_dump -h {LOCAL_DB_CONFIG['host']} -p {LOCAL_DB_CONFIG['port']} -U {LOCAL_DB_CONFIG['user']} -d {LOCAL_DB_CONFIG['database']} --data-only --column-inserts"
    
    output = run_command(cmd, "从本地 PostgreSQL 导出数据")
    if output:
        # 保存到文件
        with open('local_data_dump.sql', 'w', encoding='utf-8') as f:
            f.write(output)
        print("📁 数据已保存到 local_data_dump.sql")
        return True
    return False

def import_to_supabase():
    """导入数据到 Supabase"""
    if not os.path.exists('local_data_dump.sql'):
        print("❌ 找不到数据导出文件")
        return False
    
    # 使用 psql 导入到 Supabase
    supabase_connection = f"postgresql://postgres:{SUPABASE_SERVICE_KEY}@db.wbjbnfogbsiwqwnopocn.supabase.co:5432/postgres"
    
    cmd = f"psql '{supabase_connection}' -f local_data_dump.sql"
    
    return run_command(cmd, "导入数据到 Supabase") is not None

def check_local_data():
    """检查本地数据库中的数据"""
    password_part = f"PGPASSWORD={LOCAL_DB_CONFIG['password']}" if LOCAL_DB_CONFIG['password'] else ""
    
    # 检查用户表
    cmd = f"{password_part} psql -h {LOCAL_DB_CONFIG['host']} -p {LOCAL_DB_CONFIG['port']} -U {LOCAL_DB_CONFIG['user']} -d {LOCAL_DB_CONFIG['database']} -c 'SELECT COUNT(*) FROM users;'"
    
    result = run_command(cmd, "检查本地用户数据")
    if result:
        print(f"👥 本地用户数量: {result.strip()}")
    
    # 检查支付表
    cmd = f"{password_part} psql -h {LOCAL_DB_CONFIG['host']} -p {LOCAL_DB_CONFIG['port']} -U {LOCAL_DB_CONFIG['user']} -d {LOCAL_DB_CONFIG['database']} -c 'SELECT COUNT(*) FROM payments;'"
    
    result = run_command(cmd, "检查本地支付数据")
    if result:
        print(f"💰 本地支付记录数量: {result.strip()}")
    
    # 检查租房信息表
    cmd = f"{password_part} psql -h {LOCAL_DB_CONFIG['host']} -p {LOCAL_DB_CONFIG['port']} -U {LOCAL_DB_CONFIG['user']} -d {LOCAL_DB_CONFIG['database']} -c 'SELECT COUNT(*) FROM rent_info;'"
    
    result = run_command(cmd, "检查本地租房信息数据")
    if result:
        print(f"🏠 本地租房信息数量: {result.strip()}")
    
    # 检查工作信息表
    cmd = f"{password_part} psql -h {LOCAL_DB_CONFIG['host']} -p {LOCAL_DB_CONFIG['port']} -U {LOCAL_DB_CONFIG['user']} -d {LOCAL_DB_CONFIG['database']} -c 'SELECT COUNT(*) FROM work_info;'"
    
    result = run_command(cmd, "检查本地工作信息数据")
    if result:
        print(f"💼 本地工作信息数量: {result.strip()}")

def main():
    print("🚀 开始从本地 PostgreSQL 迁移数据到 Supabase")
    print("=" * 50)
    
    # 检查本地数据
    print("📊 检查本地数据库数据...")
    check_local_data()
    print()
    
    # 询问是否继续
    response = input("是否继续迁移数据到 Supabase? (y/N): ")
    if response.lower() != 'y':
        print("❌ 用户取消操作")
        return
    
    # 导出本地数据
    if not export_local_data():
        print("❌ 导出失败，停止迁移")
        return
    
    # 导入到 Supabase
    if import_to_supabase():
        print("🎉 数据迁移完成！")
        print("📁 数据导出文件: local_data_dump.sql")
    else:
        print("❌ 导入失败")

if __name__ == "__main__":
    main() 