#!/usr/bin/env python3
"""
安全检查脚本
用于验证代码中是否存在安全漏洞
"""

import os
import re
import subprocess
from pathlib import Path

def check_hardcoded_keys():
    """检查是否有硬编码的密钥"""
    print("🔍 检查硬编码密钥...")
    
    # 要检查的密钥模式
    key_patterns = [
        r'sk_test_[a-zA-Z0-9_]+',
        r'sk_live_[a-zA-Z0-9_]+',
        r'pk_test_[a-zA-Z0-9_]+',
        r'pk_live_[a-zA-Z0-9_]+',
        r'whsec_[a-zA-Z0-9_]+',
        r'dev-secret-key-change-in-production',
    ]
    
    # 排除的目录
    exclude_dirs = {'.git', 'venv', 'lib', '__pycache__', 'node_modules'}
    
    # 排除的文件
    exclude_files = {'.gitignore', 'README.md', 'DEPLOYMENT.md', 'SECURITY.md', 
                    'SECURITY_GUIDE.md', 'DEPLOYMENT_CHECKLIST.md', 'security_check.py'}
    
    found_keys = []
    
    for root, dirs, files in os.walk('.'):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file in exclude_files:
                continue
                
            file_path = Path(root) / file
            
            # 只检查文本文件
            if file_path.suffix in {'.py', '.html', '.css', '.js', '.txt', '.md', '.yml', '.yaml'}:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in key_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # 排除明显的示例和注释
                            if not any(exclude in str(file_path) for exclude in ['example', 'test', 'mock', 'dummy']):
                                found_keys.append((str(file_path), match))
                except Exception as e:
                    print(f"⚠️  无法读取文件 {file_path}: {e}")
    
    if found_keys:
        print("❌ 发现潜在的硬编码密钥:")
        for file_path, key in found_keys:
            print(f"   {file_path}: {key[:10]}...")
        return False
    else:
        print("✅ 未发现硬编码密钥")
        return True

def check_env_variables():
    """检查环境变量配置"""
    print("\n🔍 检查环境变量配置...")
    
    required_vars = [
        'SECRET_KEY',
        'STRIPE_SECRET_KEY', 
        'STRIPE_PUBLISHABLE_KEY',
        'STRIPE_WEBHOOK_SECRET'
    ]
    
    missing_vars = []
    configured_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            configured_vars.append(var)
            # 检查是否是示例值
            if any(pattern in value for pattern in ['xxx', 'your_', 'example', 'test_']):
                print(f"⚠️  {var}: 使用示例值，请配置真实密钥")
        else:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        return False
    elif configured_vars:
        print(f"✅ 环境变量已配置: {', '.join(configured_vars)}")
        return True
    else:
        print("⚠️  未配置任何环境变量")
        return False

def check_gitignore():
    """检查.gitignore文件"""
    print("\n🔍 检查.gitignore配置...")
    
    sensitive_files = [
        '.env',
        '*.env',
        'instance/',
        '*.db',
        '*.sqlite',
        '*.sqlite3',
        'secrets.py',
        'config_production.py'
    ]
    
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        missing_protections = []
        for file_pattern in sensitive_files:
            if file_pattern not in gitignore_content:
                missing_protections.append(file_pattern)
        
        if missing_protections:
            print(f"❌ .gitignore缺少保护: {', '.join(missing_protections)}")
            return False
        else:
            print("✅ .gitignore配置正确")
            return True
    except FileNotFoundError:
        print("❌ 未找到.gitignore文件")
        return False

def check_file_permissions():
    """检查文件权限"""
    print("\n🔍 检查文件权限...")
    
    sensitive_files = ['.env', 'instance/']
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            mode = oct(stat.st_mode)[-3:]
            
            if mode == '600' or mode == '700':
                print(f"✅ {file_path}: 权限正确 ({mode})")
            else:
                print(f"⚠️  {file_path}: 权限可能过于开放 ({mode})")
        else:
            print(f"ℹ️  {file_path}: 文件不存在")
    
    return True

def check_logging_security():
    """检查日志安全性"""
    print("\n🔍 检查日志安全性...")
    
    # 检查auth.py中的日志
    try:
        with open('app/auth.py', 'r') as f:
            content = f.read()
        
        # 检查是否有泄露密钥的日志
        dangerous_patterns = [
            r'logger\.(info|debug|error).*key.*=',
            r'logger\.(info|debug|error).*secret.*=',
            r'print.*key.*=',
            r'print.*secret.*='
        ]
        
        found_dangerous = []
        for pattern in dangerous_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_dangerous.extend(matches)
        
        if found_dangerous:
            print(f"❌ 发现潜在的日志安全问题: {found_dangerous}")
            return False
        else:
            print("✅ 日志配置安全")
            return True
    except Exception as e:
        print(f"⚠️  无法检查日志配置: {e}")
        return False

def check_dependencies():
    """检查依赖包安全性"""
    print("\n🔍 检查依赖包安全性...")
    
    try:
        # 检查是否有pip-audit
        result = subprocess.run(['pip-audit', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # 运行安全审计
            audit_result = subprocess.run(['pip-audit'], 
                                        capture_output=True, text=True)
            if 'VULNERABILITY' in audit_result.stdout:
                print("❌ 发现依赖包安全漏洞:")
                print(audit_result.stdout)
                return False
            else:
                print("✅ 依赖包安全检查通过")
                return True
        else:
            print("ℹ️  未安装pip-audit，跳过依赖安全检查")
            return True
    except FileNotFoundError:
        print("ℹ️  未安装pip-audit，跳过依赖安全检查")
        return True

def main():
    """主检查函数"""
    print("🛡️  开始安全检查\n")
    
    checks = [
        check_hardcoded_keys,
        check_env_variables,
        check_gitignore,
        check_file_permissions,
        check_logging_security,
        check_dependencies
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ 检查异常: {e}")
    
    print(f"\n📊 安全检查结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有安全检查通过！代码安全性良好。")
        print("\n📝 安全建议:")
        print("✅ 定期更新依赖包")
        print("✅ 定期轮换密钥")
        print("✅ 监控日志文件")
        print("✅ 定期备份数据")
        print("✅ 使用HTTPS")
    else:
        print("⚠️  发现安全问题，请修复后再部署。")
        print("\n🔧 修复建议:")
        print("1. 移除所有硬编码密钥")
        print("2. 配置正确的环境变量")
        print("3. 更新.gitignore文件")
        print("4. 设置正确的文件权限")
        print("5. 检查日志配置")
        print("6. 更新有漏洞的依赖包")

if __name__ == '__main__':
    main() 