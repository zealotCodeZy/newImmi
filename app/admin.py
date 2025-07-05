from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Payment
from . import db
from datetime import datetime, timedelta
import csv
import io

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """管理员权限检查装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        # 这里可以添加管理员检查逻辑
        # 例如：检查用户是否有管理员权限
        if not current_user.is_member:  # 临时使用会员权限作为管理员权限
            flash('需要管理员权限', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """管理员仪表板"""
    # 获取统计数据
    total_users = User.query.count()
    total_payments = Payment.query.count()
    active_members = User.query.filter_by(is_member=True).count()
    
    # 最近注册的用户
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # 最近的支付记录
    recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_payments=total_payments,
                         active_members=active_members,
                         recent_users=recent_users,
                         recent_payments=recent_payments)

@bp.route('/users')
@login_required
@admin_required
def users():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """添加用户"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_member = request.form.get('is_member') == 'on'
        
        if not username or not email or not password:
            flash('请填写所有必填字段', 'error')
            return render_template('admin/add_user.html')
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('admin/add_user.html')
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return render_template('admin/add_user.html')
        
        # 创建用户
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.is_member = is_member
        
        if is_member:
            # 设置会员过期时间（默认1年）
            user.membership_expires = datetime.now() + timedelta(days=365)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'用户 {username} 添加成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/add_user.html')

@bp.route('/users/bulk_add', methods=['GET', 'POST'])
@login_required
@admin_required
def bulk_add_users():
    """批量添加用户"""
    if request.method == 'POST':
        if 'csv_file' in request.files:
            # 处理CSV文件上传
            file = request.files['csv_file']
            if file.filename == '':
                flash('请选择CSV文件', 'error')
                return render_template('admin/bulk_add_users.html')
            
            if not file.filename.endswith('.csv'):
                flash('请上传CSV格式的文件', 'error')
                return render_template('admin/bulk_add_users.html')
            
            try:
                # 读取CSV文件
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        username = row.get('username', '').strip()
                        email = row.get('email', '').strip()
                        password = row.get('password', '').strip()
                        is_member = row.get('is_member', 'false').lower() == 'true'
                        
                        if not username or not email or not password:
                            errors.append(f'行 {csv_reader.line_num}: 缺少必填字段')
                            error_count += 1
                            continue
                        
                        # 检查是否已存在
                        if User.query.filter_by(username=username).first():
                            errors.append(f'行 {csv_reader.line_num}: 用户名 {username} 已存在')
                            error_count += 1
                            continue
                        
                        if User.query.filter_by(email=email).first():
                            errors.append(f'行 {csv_reader.line_num}: 邮箱 {email} 已存在')
                            error_count += 1
                            continue
                        
                        # 创建用户
                        user = User()
                        user.username = username
                        user.email = email
                        user.set_password(password)
                        user.is_member = is_member
                        
                        if is_member:
                            user.membership_expires = datetime.now() + timedelta(days=365)
                        
                        db.session.add(user)
                        success_count += 1
                        
                    except Exception as e:
                        errors.append(f'行 {csv_reader.line_num}: {str(e)}')
                        error_count += 1
                
                # 提交所有成功的用户
                if success_count > 0:
                    db.session.commit()
                
                flash(f'批量添加完成: 成功 {success_count} 个，失败 {error_count} 个', 'success')
                
                if errors:
                    flash('错误详情: ' + '; '.join(errors[:5]), 'warning')
                
                return redirect(url_for('admin.users'))
                
            except Exception as e:
                flash(f'CSV文件处理失败: {str(e)}', 'error')
                return render_template('admin/bulk_add_users.html')
        
        else:
            # 处理手动批量添加
            users_data = request.form.get('users_data', '').strip()
            if not users_data:
                flash('请输入用户数据', 'error')
                return render_template('admin/bulk_add_users.html')
            
            lines = users_data.split('\n')
            success_count = 0
            error_count = 0
            errors = []
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    # 格式: username,email,password,is_member
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 3:
                        errors.append(f'行 {i}: 格式错误，需要至少3个字段')
                        error_count += 1
                        continue
                    
                    username, email, password = parts[:3]
                    is_member = len(parts) > 3 and parts[3].lower() == 'true'
                    
                    if not username or not email or not password:
                        errors.append(f'行 {i}: 缺少必填字段')
                        error_count += 1
                        continue
                    
                    # 检查是否已存在
                    if User.query.filter_by(username=username).first():
                        errors.append(f'行 {i}: 用户名 {username} 已存在')
                        error_count += 1
                        continue
                    
                    if User.query.filter_by(email=email).first():
                        errors.append(f'行 {i}: 邮箱 {email} 已存在')
                        error_count += 1
                        continue
                    
                    # 创建用户
                    user = User()
                    user.username = username
                    user.email = email
                    user.set_password(password)
                    user.is_member = is_member
                    
                    if is_member:
                        user.membership_expires = datetime.now() + timedelta(days=365)
                    
                    db.session.add(user)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f'行 {i}: {str(e)}')
                    error_count += 1
            
            # 提交所有成功的用户
            if success_count > 0:
                db.session.commit()
            
            flash(f'批量添加完成: 成功 {success_count} 个，失败 {error_count} 个', 'success')
            
            if errors:
                flash('错误详情: ' + '; '.join(errors[:5]), 'warning')
            
            return redirect(url_for('admin.users'))
    
    return render_template('admin/bulk_add_users.html')

@bp.route('/payments')
@login_required
@admin_required
def payments():
    """支付记录管理"""
    page = request.args.get('page', 1, type=int)
    payments = Payment.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/payments.html', payments=payments)

@bp.route('/payments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_payment():
    """添加支付记录"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        amount = request.form.get('amount', type=float)
        status = request.form.get('status', 'completed')
        transaction_id = request.form.get('transaction_id', '')
        
        if not user_id or not amount:
            flash('请填写所有必填字段', 'error')
            return render_template('admin/add_payment.html')
        
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            flash('用户不存在', 'error')
            return render_template('admin/add_payment.html')
        
        # 创建支付记录
        payment = Payment()
        payment.user_id = user_id
        payment.amount = amount
        payment.status = status
        payment.transaction_id = transaction_id or f'manual_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        db.session.add(payment)
        db.session.commit()
        
        flash(f'支付记录添加成功', 'success')
        return redirect(url_for('admin.payments'))
    
    # 获取所有用户列表
    users = User.query.all()
    return render_template('admin/add_payment.html', users=users)

@bp.route('/export/users')
@login_required
@admin_required
def export_users():
    """导出用户数据"""
    users = User.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['ID', '用户名', '邮箱', '注册时间', '是否会员', '会员过期时间'])
    
    # 写入数据
    for user in users:
        writer.writerow([
            user.id,
            user.username,
            user.email,
            user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            '是' if user.is_member else '否',
            user.membership_expires.strftime('%Y-%m-%d %H:%M:%S') if user.membership_expires else ''
        ])
    
    output.seek(0)
    
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=users.csv'}
    )

@bp.route('/export/payments')
@login_required
@admin_required
def export_payments():
    """导出支付数据"""
    payments = Payment.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['ID', '用户ID', '用户名', '金额', '状态', '交易ID', '支付时间'])
    
    # 写入数据
    for payment in payments:
        writer.writerow([
            payment.id,
            payment.user_id,
            payment.user.username if payment.user else '',
            payment.amount,
            payment.status,
            payment.transaction_id,
            payment.payment_date.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_date else ''
        ])
    
    output.seek(0)
    
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=payments.csv'}
    ) 