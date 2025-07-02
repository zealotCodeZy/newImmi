from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from .models import User, Payment
from . import db
from datetime import datetime, timedelta
from config import Config
import uuid
import stripe

bp = Blueprint('auth', __name__)

# Stripe配置
stripe.api_key = Config.STRIPE_SECRET_KEY

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('密码不匹配', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return render_template('auth/register.html')
        
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('用户名或密码错误', 'error')
            return render_template('auth/login.html')
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/membership')
@login_required
def membership():
    return render_template('auth/membership.html')

@bp.route('/payment', methods=['POST'])
@login_required
def payment():
    # 获取付费类型
    plan = request.form.get('plan', 'year')
    if plan == 'month':
        amount = Config.MEMBERSHIP_PRICE_MONTH
        expires = datetime.utcnow() + timedelta(days=31)
        plan_label = '月付'
    else:
        amount = Config.MEMBERSHIP_PRICE_YEAR
        expires = datetime.utcnow() + timedelta(days=365)
        plan_label = '年付'
    
    transaction_id = str(uuid.uuid4())
    payment = Payment(
        user_id=current_user.id,
        amount=amount,
        status='completed',
        transaction_id=transaction_id
    )
    # 更新用户会员状态
    current_user.is_member = True
    current_user.membership_expires = expires
    db.session.add(payment)
    db.session.commit()
    flash(f'支付成功！您已成为{plan_label}会员，可以访问所有功能', 'success')
    return redirect(url_for('main.rentBlack'))

@bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    data = request.get_json() or {}
    plan = data.get('plan', 'year')
    if plan == 'month':
        amount = int(Config.MEMBERSHIP_PRICE_MONTH * 100)
        desc = '会员月付'
    else:
        amount = int(Config.MEMBERSHIP_PRICE_YEAR * 100)
        desc = '会员年付'
    # Stripe金额单位为分
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card', 'alipay', 'wechat_pay'],
        description=desc,
        metadata={'user_id': current_user.id, 'plan': plan}
    )
    return jsonify({
        'clientSecret': intent.client_secret,
        'publishableKey': Config.STRIPE_PUBLISHABLE_KEY
    }) 