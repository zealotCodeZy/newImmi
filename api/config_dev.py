import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class DevConfig:
    # 强制要求设置SECRET_KEY，不允许使用默认值
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MEMBERSHIP_PRICE_YEAR = 9.99  # 年付会员价格
    MEMBERSHIP_PRICE_MONTH = 0.99  # 月付会员价格
    
    # 强制要求设置Stripe密钥，不允许使用默认值
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test')
    if not STRIPE_SECRET_KEY:
        raise ValueError("STRIPE_SECRET_KEY environment variable is required")
    
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test')
    if not STRIPE_PUBLISHABLE_KEY:
        raise ValueError("STRIPE_PUBLISHABLE_KEY environment variable is required") 