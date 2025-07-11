#!/usr/bin/env python3
import os
import re

# 新的 API 基础 URL
NEW_API_BASE = "https://api-vercel-1i4wawkir-zealotcodezys-projects.vercel.app/api"

# 需要更新的文件类型
FILE_EXTENSIONS = ['.html', '.js']

def update_api_endpoints():
    """批量更新前端代码中的 API 端点"""
    
    # 遍历 static_site 目录
    for root, dirs, files in os.walk('static_site'):
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                file_path = os.path.join(root, file)
                print(f"处理文件: {file_path}")
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 替换 API 端点
                original_content = content
                
                # 替换 localhost:5002 的 API 调用
                content = re.sub(
                    r'http://localhost:5002/api',
                    NEW_API_BASE,
                    content
                )
                
                # 替换相对路径的 API 调用（如 /api/rent-blacklist）
                content = re.sub(
                    r'fetch\([\'"`]/api/',
                    f'fetch(\'{NEW_API_BASE}/',
                    content
                )
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✓ 已更新: {file_path}")
                else:
                    print(f"  - 无需更新: {file_path}")

if __name__ == "__main__":
    update_api_endpoints()
    print("\n✅ API 端点更新完成！") 