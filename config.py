import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///membership.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEMBERSHIP_PRICE_YEAR = 9.99  # 年付会员价格
    MEMBERSHIP_PRICE_MONTH = 1.99  # 月付会员价格
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_xxx'
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY') or 'pk_test_xxx'


