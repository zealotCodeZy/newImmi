from flask import Blueprint, redirect, url_for, flash, request, jsonify, current_app
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

# 只保留API路由
@bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not all([username, email, password, confirm_password]):
        return jsonify(success=False, message='缺少参数'), 400
    if password != confirm_password:
        return jsonify(success=False, message='密码不匹配'), 400
    if User.query.filter_by(username=username).first():
        return jsonify(success=False, message='用户名已存在'), 400
    if User.query.filter_by(email=email).first():
        return jsonify(success=False, message='邮箱已被注册'), 400
    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message='注册失败，数据库写入异常'), 500
    return jsonify(success=True, message='注册成功')

@bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return jsonify(success=False, message='缺少参数'), 400
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message='用户名或密码错误'), 401
    login_user(user)
    return jsonify(success=True, message='登录成功')

@bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify(success=True, message='已登出')

@bp.route('/api/membership', methods=['GET'])
@login_required
def api_membership():
    return jsonify(success=True, is_member=current_user.is_member, expires=str(current_user.membership_expires) if current_user.membership_expires else None)

@bp.route('/api/payment', methods=['POST'])
@login_required
def api_payment():
    try:
        plan = request.json.get('plan', 'year')
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
        current_user.is_member = True
        current_user.membership_expires = expires
        db.session.add(payment)
        db.session.commit()
        logger.info(f"用户 {current_user.username} 成功购买 {plan_label} 会员")
        return jsonify(success=True, message=f'支付成功！您已成为{plan_label}会员，可以访问所有功能')
    except Exception as e:
        logger.error(f"支付处理失败: {str(e)}")
        db.session.rollback()
        return jsonify(success=False, message='支付处理失败，请重试'), 500

@bp.route('/api/create-payment-intent', methods=['POST'])
@login_required
def api_create_payment_intent():
    try:
        data = request.get_json() or {}
        plan = data.get('plan', 'year')
        if plan == 'month':
            amount = int(Config.MEMBERSHIP_PRICE_MONTH * 100)
            desc = '会员月付'
        else:
            amount = int(Config.MEMBERSHIP_PRICE_YEAR * 100)
            desc = '会员年付'
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