import os

class Config:
    # 强制要求设置SECRET_KEY，不允许使用默认值
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'membership.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLite生产环境优化配置
    if 'sqlite' in (os.environ.get('DATABASE_URL') or '').lower() or 'sqlite' in SQLALCHEMY_DATABASE_URI.lower():
        # 启用SQLite WAL模式，提高并发性能
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,  # 连接前检查
            'pool_recycle': 300,    # 5分钟回收连接
            'pool_size': 10,        # 连接池大小
            'max_overflow': 20,     # 最大溢出连接
            'connect_args': {
                'timeout': 30,      # 连接超时
                'check_same_thread': False,  # 允许多线程
                'isolation_level': None,     # 自动提交
            }
        }
    
    MEMBERSHIP_PRICE_YEAR = 9.99  # 年付会员价格
    MEMBERSHIP_PRICE_MONTH = 1.99  # 月付会员价格
    
    # 强制要求设置Stripe密钥，不允许使用默认值
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    if not STRIPE_SECRET_KEY:
        raise ValueError("STRIPE_SECRET_KEY environment variable is required")
    
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    if not STRIPE_PUBLISHABLE_KEY:
        raise ValueError("STRIPE_PUBLISHABLE_KEY environment variable is required")


