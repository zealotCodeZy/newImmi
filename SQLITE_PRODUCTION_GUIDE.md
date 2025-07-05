# SQLite生产环境使用指南

## ✅ 为什么SQLite适合你的项目？

### 数据规模分析
- **用户数量**: 预计1000条记录
- **支付记录**: 预计1000-2000条记录
- **查询复杂度**: 简单到中等复杂度
- **并发量**: 低到中等并发

### SQLite优势
- ✅ **简单可靠**: 单文件存储，无需额外服务
- ✅ **性能足够**: 1000条记录查询速度 < 1ms
- ✅ **部署简单**: 减少系统复杂度
- ✅ **成本低廉**: 无需数据库服务器
- ✅ **备份简单**: 直接复制文件即可

## 🔧 生产环境优化配置

### 1. 数据库配置优化

已在 `config.py` 中添加了生产环境优化：

```python
# SQLite生产环境优化配置
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,      # 连接前检查
    'pool_recycle': 300,        # 5分钟回收连接
    'pool_size': 10,            # 连接池大小
    'max_overflow': 20,         # 最大溢出连接
    'connect_args': {
        'timeout': 30,          # 连接超时
        'check_same_thread': False,  # 允许多线程
        'isolation_level': None,     # 自动提交
    }
}
```

### 2. 数据库文件优化

运行优化脚本：
```bash
python optimize_sqlite.py
```

这个脚本会：
- 启用WAL模式（提高并发性能）
- 优化缓存和同步设置
- 分析表结构
- 创建备份
- 性能测试

## 📊 性能基准测试

### 预期性能指标
- **用户查询**: < 1ms
- **支付查询**: < 1ms  
- **复杂JOIN查询**: < 5ms
- **并发写入**: 支持10-20个并发用户

### 实际测试结果
运行 `python optimize_sqlite.py` 查看实际性能数据。

## 🛡️ 安全配置

### 1. 文件权限
```bash
# 设置正确的文件权限
chmod 600 instance/membership.db
chmod 700 instance/
chown www-data:www-data instance/
```

### 2. 备份策略
```bash
# 每日备份
cp instance/membership.db instance/backup_$(date +%Y%m%d).db

# 或使用优化脚本自动备份
python optimize_sqlite.py
```

### 3. 监控WAL文件
```bash
# 检查WAL文件大小
ls -la instance/membership.db*

# 如果WAL文件过大，可以压缩
sqlite3 instance/membership.db "VACUUM;"
```

## 📈 扩展性考虑

### 何时考虑迁移到PostgreSQL？

**建议迁移的指标：**
- 用户数量 > 10,000
- 支付记录 > 50,000
- 并发用户 > 100
- 查询响应时间 > 100ms
- 数据库文件大小 > 1GB

**迁移准备：**
- 保持数据库结构标准化
- 使用SQLAlchemy ORM（已实现）
- 定期备份数据
- 监控性能指标

## 🔄 维护操作

### 1. 定期维护
```bash
# 每周运行一次
python optimize_sqlite.py

# 每月清理一次
sqlite3 instance/membership.db "VACUUM; ANALYZE;"
```

### 2. 性能监控
```bash
# 检查数据库大小
du -h instance/membership.db

# 检查表记录数
sqlite3 instance/membership.db "SELECT COUNT(*) FROM user; SELECT COUNT(*) FROM payment;"
```

### 3. 备份恢复
```bash
# 创建备份
cp instance/membership.db instance/backup_$(date +%Y%m%d_%H%M%S).db

# 恢复备份
cp instance/backup_20241201_120000.db instance/membership.db
```

## 🚀 部署配置

### 1. 环境变量设置
```bash
# 使用SQLite（默认）
export DATABASE_URL="sqlite:///instance/membership.db"

# 或指定绝对路径
export DATABASE_URL="sqlite:////path/to/your/project/instance/membership.db"
```

### 2. 启动应用
```bash
# 使用部署脚本（推荐）
chmod +x deploy.sh
./deploy.sh

# 或手动启动
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 3. 监控日志
```bash
# 监控应用日志
tail -f /var/log/newimmi/app.log

# 监控数据库文件变化
watch -n 5 "ls -la instance/"
```

## ⚠️ 注意事项

### 1. 并发限制
- SQLite使用文件锁，同时只能有一个写操作
- 对于你的应用场景（用户注册、支付处理），这个限制通常不是问题
- 如果遇到并发问题，考虑使用队列或延迟处理

### 2. 文件系统
- 确保文件系统支持文件锁
- 避免使用网络文件系统（NFS）
- 推荐使用本地SSD存储

### 3. 备份策略
- 定期备份数据库文件
- 备份时停止应用或使用WAL模式
- 测试备份文件的完整性

## 📝 最佳实践

### 1. 开发环境
- 使用相同的SQLite配置
- 定期同步生产数据结构
- 使用测试数据验证性能

### 2. 生产环境
- 定期运行优化脚本
- 监控数据库文件大小
- 设置自动备份
- 记录性能指标

### 3. 故障处理
- 保留多个备份版本
- 准备快速恢复脚本
- 监控磁盘空间

## 🎯 结论

对于你的项目（1000条记录），**SQLite完全适合生产环境**！

**优势：**
- 部署简单，维护成本低
- 性能足够，响应速度快
- 可靠性高，数据一致性好
- 备份简单，恢复快速

**建议：**
1. 使用提供的优化配置
2. 定期运行维护脚本
3. 监控性能指标
4. 准备扩展计划（当数据量增长时）

SQLite是一个成熟、可靠的数据库选择，特别适合中小型应用。你的项目完全可以使用SQLite进行生产部署！ 