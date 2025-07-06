# 新移民防踩坑 - 会员系统

这是一个为移民提供租房黑名单查询等服务的网站，采用会员付费模式。

## 功能特性

### 🔐 用户认证系统
- 用户注册和登录
- 密码加密存储
- 会话管理

### 💎 会员付费系统
- 会员价格：$9.99/年 或 $0.99/月
- 模拟支付处理
- 会员状态管理
- 自动过期处理

### 🛡️ 访问控制
- 租房黑名单查询需要会员权限
- 自动重定向未登录用户
- 会员状态验证

## 技术栈

- **后端**: Flask 2.3.2
- **数据库**: SQLite (通过 Flask-SQLAlchemy)
- **认证**: Flask-Login
- **模板引擎**: Jinja2
- **样式**: 自定义 CSS

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python main.py
```

应用将在 `http://127.0.0.1:5002` 启动

## 使用流程

### 1. 访问受保护页面
访问 `http://127.0.0.1:5002/rentBlack`，系统会自动重定向到登录页面。

### 2. 注册新用户
- 点击"立即注册"
- 填写用户名、邮箱和密码
- 提交注册表单

### 3. 用户登录
- 输入用户名和密码
- 点击登录按钮

### 4. 购买会员
- 登录后访问会员购买页面
- 填写支付信息（模拟）
- 完成支付

### 5. 使用会员功能
付费成功后，即可访问租房黑名单查询功能。

## 数据库结构

### User 表
- `id`: 主键
- `username`: 用户名（唯一）
- `email`: 邮箱（唯一）
- `password_hash`: 密码哈希
- `created_at`: 创建时间
- `is_member`: 会员状态
- `membership_expires`: 会员过期时间

### Payment 表
- `id`: 主键
- `user_id`: 用户ID（外键）
- `amount`: 支付金额
- `payment_date`: 支付时间
- `status`: 支付状态
- `transaction_id`: 交易ID

## 文件结构

```
newImmi/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── routes.py            # 主路由
│   ├── auth.py              # 认证路由
│   ├── models.py            # 数据模型
│   ├── utils.py             # 工具函数
│   ├── static/
│   │   └── style.css        # 样式文件
│   └── templates/
│       ├── base.html        # 基础模板
│       ├── rentBlack.html   # 租房黑名单页面
│       └── auth/
│           ├── login.html   # 登录页面
│           ├── register.html # 注册页面
│           └── membership.html # 会员购买页面
├── config.py                # 配置文件
├── main.py                  # 应用入口
├── requirements.txt         # 依赖列表
└── README.md               # 说明文档
```

## 安全特性

- 密码使用 Werkzeug 的 `generate_password_hash` 加密
- 使用 Flask-Login 进行会话管理
- 防止未授权访问的装饰器
- 会员状态实时验证

## 测试

运行测试脚本：
```bash
python test_membership.py
```

## 部署

### 生产环境部署
```bash
gunicorn -w 4 -b 0.0.0.0:5002 main:app
```

### 环境变量
- `SECRET_KEY`: 应用密钥
- `DATABASE_URL`: 数据库连接字符串

## 注意事项

1. 当前支付系统为模拟实现，实际部署需要集成真实的支付网关
2. 数据库使用 SQLite，生产环境建议使用 PostgreSQL 或 MySQL
3. 会员价格为 $9.99/年 或 $0.99/月，可在 `config.py` 中修改
4. 会员有效期为 365 天，可在 `auth.py` 中修改

## 许可证

Copyright ©2025 新移民第一站 All Rights Reserved 