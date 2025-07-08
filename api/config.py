import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 强制要求设置SECRET_KEY，不允许使用默认值
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    SQLALCHEMY_DATABASE_URI = "postgresql://newimmi_user:AlbertFreeman!@127.0.0.1:5432/newimmi_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MEMBERSHIP_PRICE_YEAR = 9.99  # 年付会员价格
    MEMBERSHIP_PRICE_MONTH = 0.99  # 月付会员价格
    
    # 强制要求设置Stripe密钥，不允许使用默认值
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    if not STRIPE_SECRET_KEY:
        raise ValueError("STRIPE_SECRET_KEY environment variable is required")
    
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    if not STRIPE_PUBLISHABLE_KEY:
        raise ValueError("STRIPE_PUBLISHABLE_KEY environment variable is required")


