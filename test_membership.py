#!/usr/bin/env python3
"""
会员系统测试脚本
演示完整的注册、登录、付费流程
"""

import requests
import time

BASE_URL = "http://127.0.0.1:5002"

def test_membership_flow():
    """测试完整的会员流程"""
    session = requests.Session()
    
    print("=== 新移民防踩坑 - 会员系统测试 ===\n")
    
    # 1. 测试访问受保护的页面（应该重定向到登录）
    print("1. 测试访问租房黑名单页面（未登录）...")
    response = session.get(f"{BASE_URL}/rentBlack", allow_redirects=False)
    if response.status_code == 302:
        print("✅ 正确重定向到登录页面")
    else:
        print("❌ 未正确重定向")
    
    # 2. 访问登录页面
    print("\n2. 访问登录页面...")
    response = session.get(f"{BASE_URL}/auth/login")
    if response.status_code == 200:
        print("✅ 登录页面可访问")
    else:
        print("❌ 登录页面无法访问")
    
    # 3. 访问注册页面
    print("\n3. 访问注册页面...")
    response = session.get(f"{BASE_URL}/auth/register")
    if response.status_code == 200:
        print("✅ 注册页面可访问")
    else:
        print("❌ 注册页面无法访问")
    
    # 4. 测试注册功能
    print("\n4. 测试用户注册...")
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    response = session.post(f"{BASE_URL}/auth/register", data=register_data, allow_redirects=False)
    if response.status_code == 302:
        print("✅ 注册成功，重定向到登录页面")
    else:
        print("❌ 注册失败")
    
    # 5. 测试登录功能
    print("\n5. 测试用户登录...")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=False)
    if response.status_code == 302:
        print("✅ 登录成功")
    else:
        print("❌ 登录失败")
    
    # 6. 测试访问会员页面
    print("\n6. 测试访问会员购买页面...")
    response = session.get(f"{BASE_URL}/auth/membership")
    if response.status_code == 200:
        print("✅ 会员页面可访问")
    else:
        print("❌ 会员页面无法访问")
    
    # 7. 测试付费功能
    print("\n7. 测试会员付费...")
    payment_data = {
        'card_number': '4111111111111111',
        'expiry': '12/25',
        'cvv': '123',
        'name': 'Test User'
    }
    response = session.post(f"{BASE_URL}/auth/payment", data=payment_data, allow_redirects=False)
    if response.status_code == 302:
        print("✅ 付费成功，重定向到租房黑名单页面")
    else:
        print("❌ 付费失败")
    
    # 8. 测试访问受保护的页面（已付费）
    print("\n8. 测试访问租房黑名单页面（已付费会员）...")
    response = session.get(f"{BASE_URL}/rentBlack")
    if response.status_code == 200:
        print("✅ 可以访问租房黑名单页面")
    else:
        print("❌ 无法访问租房黑名单页面")
    
    print("\n=== 测试完成 ===")
    print("\n使用说明：")
    print("1. 访问 http://127.0.0.1:5002/rentBlack")
    print("2. 系统会自动重定向到登录页面")
    print("3. 点击'立即注册'创建新账号")
    print("4. 登录后点击'会员购买'进行付费")
    print("5. 付费成功后即可访问租房黑名单功能")

if __name__ == "__main__":
    test_membership_flow() 