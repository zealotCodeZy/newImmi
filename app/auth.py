from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from .models import User, Payment
from . import db
from datetime import datetime, timedelta, timezone
from config import Config
import uuid
import stripe
import os
import stripe.error
import logging
import traceback

bp = Blueprint('auth', __name__)

# 配置日志
logger = logging.getLogger(__name__)

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
        try:
            print('即将 commit')
            db.session.commit()
            print('commit 完成')
        except Exception as e:
            print('commit 失败:', e)
            print(traceback.format_exc())
            db.session.rollback()
            flash('注册失败，数据库写入异常', 'error')
            return render_template('auth/register.html')
        
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
    try:
        # 获取付费类型
        plan = request.form.get('plan', 'year')
        if plan == 'month':
            amount = Config.MEMBERSHIP_PRICE_MONTH
            expires = datetime.now(timezone.utc) + timedelta(days=31)
            plan_label = '月付'
        else:
            amount = Config.MEMBERSHIP_PRICE_YEAR
            expires = datetime.now(timezone.utc) + timedelta(days=365)
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
        
        logger.info(f"用户 {current_user.username} 成功购买 {plan_label} 会员")
        flash(f'支付成功！您已成为{plan_label}会员，可以访问所有功能', 'success')
        return redirect(url_for('main.rentBlack'))
    except Exception as e:
        logger.error(f"支付处理失败: {str(e)}")
        db.session.rollback()
        flash('支付处理失败，请重试', 'error')
        return redirect(url_for('auth.membership'))

@bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    try:
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
            metadata={
                'user_id': current_user.id, 
                'plan': plan,
                'username': current_user.username
            }
        )
        
        logger.info(f"为用户 {current_user.username} 创建支付意图: {intent.id}")
        return jsonify({
            'clientSecret': intent.client_secret,
            'publishableKey': Config.STRIPE_PUBLISHABLE_KEY
        })
    except stripe.StripeError as e:
        logger.error(f"Stripe错误: {str(e)}")
        return jsonify({'error': '支付服务暂时不可用'}), 500
    except Exception as e:
        logger.error(f"创建支付意图失败: {str(e)}")
        return jsonify({'error': '服务器错误'}), 500

# Stripe Webhook 回调
@bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    if not endpoint_secret:
        logger.error("STRIPE_WEBHOOK_SECRET environment variable is required")
        return 'Webhook secret not configured', 500
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        logger.error(f"Webhook payload无效: {str(e)}")
        return 'Invalid payload', 400
    except stripe.SignatureVerificationError as e:
        logger.error(f"Webhook签名验证失败: {str(e)}")
        return 'Invalid signature', 400

    # 处理支付成功事件
    if event['type'] == 'payment_intent.succeeded':
        try:
            intent = event['data']['object']
            user_id = intent['metadata'].get('user_id')
            plan = intent['metadata'].get('plan', 'year')
            username = intent['metadata'].get('username', 'unknown')
            
            if not user_id:
                logger.error("Webhook中缺少user_id")
                return 'Missing user_id', 400
            
            user = User.query.get(int(user_id))
            if not user:
                logger.error(f"用户不存在: {user_id}")
                return 'User not found', 404
            
            # 检查是否已经处理过这个支付
            existing_payment = Payment.query.filter_by(transaction_id=intent['id']).first()
            if existing_payment:
                logger.info(f"支付 {intent['id']} 已经处理过")
                return '', 200
            
            # 设置会员过期时间
            if plan == 'month':
                expires = datetime.now(timezone.utc) + timedelta(days=31)
                amount = Config.MEMBERSHIP_PRICE_MONTH
            else:
                expires = datetime.now(timezone.utc) + timedelta(days=365)
                amount = Config.MEMBERSHIP_PRICE_YEAR
            
            # 更新用户会员状态
            user.is_member = True
            user.membership_expires = expires
            
            # 创建支付记录
            payment = Payment(
                user_id=user.id,
                amount=amount,
                status='completed',
                transaction_id=intent['id']
            )
            
            db.session.add(payment)
            db.session.commit()
            
            logger.info(f"Webhook处理成功: 用户 {username} 成为会员，支付ID: {intent['id']}")
            
        except Exception as e:
            logger.error(f"Webhook处理失败: {str(e)}")
            db.session.rollback()
            return 'Webhook processing failed', 500
    
    # 处理支付失败事件
    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        user_id = intent['metadata'].get('user_id')
        username = intent['metadata'].get('username', 'unknown')
        logger.warning(f"支付失败: 用户 {username}, 支付ID: {intent['id']}")
    
    return '', 200 