# 数据输入指南

## 📝 数据输入方法总览

### 1. **Web界面管理（推荐）**
- 访问 `/admin` 路径进行可视化数据管理
- 支持单个添加和批量导入
- 实时查看和编辑数据

### 2. **命令行脚本**
- 使用 `python data_input.py` 进行交互式数据输入
- 支持批量添加示例数据
- 适合快速测试和开发

### 3. **CSV批量导入**
- 准备CSV文件，通过Web界面批量导入
- 适合大量数据迁移
- 支持错误检查和报告

### 4. **直接SQL操作**
- 使用SQLite命令行工具直接操作数据库
- 适合高级用户和复杂操作

## 🖥️ Web界面管理

### 访问管理员界面
1. 启动应用：`python main.py`
2. 访问：`http://localhost:5000/admin`
3. 使用会员账户登录（临时使用会员权限作为管理员权限）

### 功能列表
- **仪表板**: 查看统计数据
- **用户管理**: 添加、编辑、删除用户
- **支付管理**: 管理支付记录
- **数据导出**: 导出CSV格式数据

### 批量添加用户
1. 访问 `/admin/users/bulk_add`
2. 选择CSV文件上传或手动输入数据
3. 格式：`username,email,password,is_member`

## 💻 命令行脚本

### 运行脚本
```bash
python data_input.py
```

### 功能选项
1. **添加示例用户**: 快速添加测试用户
2. **添加示例支付记录**: 添加测试支付数据
3. **交互式添加用户**: 逐个添加用户
4. **显示数据库统计**: 查看当前数据状态

### 示例用户数据
脚本会自动添加以下示例用户：
- `admin` / `admin123` (管理员)
- `testuser1` / `password123` (会员用户)
- `testuser2` / `password123` (普通用户)
- `vipuser` / `vip123` (VIP会员)

## 📊 CSV批量导入

### CSV文件格式
```csv
username,email,password,is_member
user1,user1@example.com,password123,true
user2,user2@example.com,password123,false
user3,user3@example.com,password123,true
```

### 字段说明
- `username`: 用户名（必填，唯一）
- `email`: 邮箱地址（必填，唯一）
- `password`: 密码（必填）
- `is_member`: 是否会员（可选，true/false）

### 使用步骤
1. 准备CSV文件（参考 `templates/users_template.csv`）
2. 访问 `/admin/users/bulk_add`
3. 上传CSV文件
4. 查看导入结果和错误报告

## 🔧 直接SQL操作

### 连接数据库
```bash
sqlite3 instance/membership.db
```

### 常用SQL命令
```sql
-- 查看所有用户
SELECT * FROM user;

-- 查看所有支付记录
SELECT * FROM payment;

-- 添加用户
INSERT INTO user (username, email, password_hash, created_at, is_member) 
VALUES ('newuser', 'newuser@example.com', 'hashed_password', datetime('now'), 0);

-- 更新用户为会员
UPDATE user SET is_member = 1, membership_expires = datetime('now', '+1 year') 
WHERE username = 'newuser';

-- 查看统计信息
SELECT COUNT(*) as total_users FROM user;
SELECT COUNT(*) as total_payments FROM payment;
SELECT COUNT(*) as active_members FROM user WHERE is_member = 1;
```

## 📋 数据输入最佳实践

### 1. **开发环境**
- 使用 `python data_input.py` 快速添加测试数据
- 使用示例用户进行功能测试
- 定期清理测试数据

### 2. **生产环境**
- 使用Web界面进行数据管理
- 通过CSV批量导入大量数据
- 定期备份数据库

### 3. **数据验证**
- 检查用户名和邮箱唯一性
- 验证密码强度
- 确认会员状态设置

### 4. **错误处理**
- 查看导入错误报告
- 手动修复重复数据
- 验证数据完整性

## 🚀 快速开始

### 方法1：使用脚本（最简单）
```bash
# 1. 运行数据输入脚本
python data_input.py

# 2. 选择选项1添加示例用户
# 3. 选择选项2添加示例支付记录
# 4. 选择选项4查看统计信息
```

### 方法2：使用Web界面
```bash
# 1. 启动应用
python main.py

# 2. 注册一个用户并购买会员
# 3. 访问 http://localhost:5000/admin
# 4. 使用会员账户登录
# 5. 在管理界面添加数据
```

### 方法3：使用CSV导入
```bash
# 1. 编辑 templates/users_template.csv
# 2. 启动应用
python main.py

# 3. 访问 http://localhost:5000/admin/users/bulk_add
# 4. 上传CSV文件
```

## ⚠️ 注意事项

### 1. **数据安全**
- 生产环境不要使用示例密码
- 定期更改管理员密码
- 备份重要数据

### 2. **性能考虑**
- 批量导入大量数据时，建议分批进行
- 避免在高峰时段进行大量数据操作
- 监控数据库文件大小

### 3. **数据一致性**
- 确保用户名和邮箱唯一性
- 验证外键关系（支付记录关联用户）
- 检查会员过期时间设置

## 🔍 故障排除

### 常见问题
1. **用户名已存在**: 检查是否重复，或使用不同用户名
2. **邮箱已被注册**: 使用不同的邮箱地址
3. **CSV格式错误**: 检查字段分隔符和编码格式
4. **权限不足**: 确保使用会员账户访问管理界面

### 调试命令
```bash
# 检查数据库文件
ls -la instance/

# 查看数据库内容
sqlite3 instance/membership.db ".tables"
sqlite3 instance/membership.db "SELECT * FROM user;"

# 重置数据库（谨慎使用）
rm instance/membership.db
python main.py  # 重新创建数据库
```

## 📞 获取帮助

如果遇到问题：
1. 查看错误信息和日志
2. 检查数据格式是否正确
3. 验证数据库文件权限
4. 参考本文档的故障排除部分

数据输入工具已经为你提供了多种便捷的方式，选择最适合你的方法即可！ 