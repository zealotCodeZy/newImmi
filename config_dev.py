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
    
    # 简化的SQLite配置，避免连接问题
    if 'sqlite' in (os.environ.get('DATABASE_URL') or '').lower() or 'sqlite' in SQLALCHEMY_DATABASE_URI.lower():
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'timeout': 30,
            }
        }
    
    MEMBERSHIP_PRICE_YEAR = 9.99  # 年付会员价格
    MEMBERSHIP_PRICE_MONTH = 0.99  # 月付会员价格
    
    # 强制要求设置Stripe密钥，不允许使用默认值
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    if not STRIPE_SECRET_KEY:
        raise ValueError("STRIPE_SECRET_KEY environment variable is required")
    
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    if not STRIPE_PUBLISHABLE_KEY:
        raise ValueError("STRIPE_PUBLISHABLE_KEY environment variable is required") 