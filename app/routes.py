from flask import render_template, request, Blueprint, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import RentInfo, WorkInfo
from . import db

bp = Blueprint('main', __name__)

def membership_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_membership_active():
            flash('此功能需要会员权限，请先购买会员', 'warning')
            return redirect(url_for('auth.membership'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/rent')
def rent():
    return render_template('rent.html')

@bp.route('/rentBlack')
@login_required
@membership_required
def rentBlack():
    return render_template('rentBlack.html')

@bp.route('/rentResult', methods=['POST'])
@login_required
@membership_required
def rentResult():
    zipcode = request.form['zipcode']
    # 查询所有该zipcode的黑名单房源地址
    addresses = [r.address for r in RentInfo.query.filter_by(zipcode=zipcode).all()]
    return render_template('rentResult.html', zipcode=zipcode, addresses=addresses)

@bp.route('/rentDetail/<address>')
@login_required
@membership_required
def rentDetail(address):
    # 查询该地址的黑名单详情
    info = RentInfo.query.filter_by(address=address).first()
    if info:
        return render_template('rentDetail.html', info=info)
    else:
        abort(404)

@bp.route('/work')
def work():
    return render_template('work.html')

@bp.route('/workBlack')
@login_required
@membership_required
def workBlack():
    return render_template('workBlack.html')

@bp.route('/workResult', methods=['POST'])
def workResult():
    name = request.form['name']
    # 查询所有公司名包含name的黑名单公司
    names = [w.name for w in WorkInfo.query.filter(WorkInfo.name.ilike(f'%{name}%')).all()]
    return render_template('workResult.html', name=name, names=names)

@bp.route('/workDetail/<name>')
def workDetail(name):
    # 查询公司名为name的黑名单详情
    info = WorkInfo.query.filter_by(name=name).first()
    if info:
        return render_template('workDetail.html', info=info)
    else:
        abort(404)

@bp.route('/contact')
def about():
    return render_template('contact.html')

@bp.route('/tel')
def tel():
    return render_template('tel.html')

@bp.route('/drive')
def drive():
    return render_template('drive.html')

@bp.route('/bank')
def bank():
    return render_template('bank.html')

@bp.route('/id')
def id_page():
    return render_template('id.html')

@bp.route('/res')
def res():
    return render_template('res.html')