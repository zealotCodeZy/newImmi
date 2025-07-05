import sqlite3
import os
import re

def get_db_connection():
    # 获取instance目录的路径
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    db_path = os.path.join(instance_path, 'blacklist.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def validate_zipcode(zipcode):
    """验证邮编格式"""
    if not zipcode or not isinstance(zipcode, str):
        return False
    # 只允许5位数字
    return bool(re.match(r'^\d{5}$', zipcode.strip()))

def validate_company_name(name):
    """验证公司名称格式"""
    if not name or not isinstance(name, str):
        return False
    # 只允许中英文字母，不允许数字、符号、空格
    return bool(re.match(r'^[\u4e00-\u9fa5a-zA-Z]+$', name.strip()))

def sanitize_input(input_str, max_length=100):
    """清理输入字符串"""
    if not input_str:
        return ""
    # 移除首尾空格，限制长度
    cleaned = str(input_str).strip()[:max_length]
    return cleaned

def get_addresses_rent(zipcode):
    # 验证输入
    if not validate_zipcode(zipcode):
        return []
    
    zipcode = sanitize_input(zipcode, 5)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT address FROM rent_info WHERE zipcode = ?", (zipcode,))
        addresses = [row['address'] for row in cursor.fetchall()]
        conn.close()
        return addresses
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return []

def get_info_rent(address):
    # 验证输入
    if not address or not isinstance(address, str):
        return None
    
    address = sanitize_input(address, 200)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT zipcode, address, content FROM rent_info WHERE address = ?", (address,))
        info = cursor.fetchone()
        conn.close()
        return dict(info) if info else None
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return None

def get_name_work(name):
    # 验证输入
    if not validate_company_name(name):
        return []
    
    name = sanitize_input(name, 50)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM work_info WHERE name like ?", ('%' + name + '%',))
        names = [row['name'] for row in cursor.fetchall()]
        conn.close()
        return names
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return []

def get_info_work(name):
    # 验证输入
    if not validate_company_name(name):
        return None
    
    name = sanitize_input(name, 50)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM work_info WHERE name = ?", (name,))
        info = cursor.fetchone()
        conn.close()
        return dict(info) if info else None
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return None