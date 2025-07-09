from flask import request, Blueprint, abort, jsonify
from flask_login import login_required, current_user
from functools import wraps
from .models import RentInfo, WorkInfo
from . import db

bp = Blueprint('main', __name__)

def membership_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify(success=False, message='需要登录'), 401
        if not current_user.is_membership_active():
            return jsonify(success=False, message='需要会员权限'), 403
        return f(*args, **kwargs)
    return decorated_function

# 检查用户认证状态
@bp.route('/api/check-auth', methods=['GET'])
def check_auth():
    if not current_user.is_authenticated:
        return jsonify(authenticated=False, membership_active=False)
    return jsonify(
        authenticated=True, 
        membership_active=current_user.is_membership_active()
    )

# 只保留API路由
@bp.route('/api/rent', methods=['GET'])
@membership_required
def api_rent():
    zipcode = request.args.get('zipcode')
    if not zipcode:
        return jsonify(success=False, message='缺少zipcode参数'), 400
    addresses = [r.address for r in RentInfo.query.filter_by(zipcode=zipcode).all()]
    return jsonify(success=True, data={'addresses': addresses})

@bp.route('/api/rentDetail/<address>', methods=['GET'])
@membership_required
def api_rent_detail(address):
    info = RentInfo.query.filter_by(address=address).first()
    if info:
        return jsonify(success=True, data={'address': info.address, 'content': info.content})
    else:
        return jsonify(success=False, message='未找到该地址'), 404

@bp.route('/api/work', methods=['GET'])
@membership_required
def api_work():
    zipcode = request.args.get('zipcode')
    works = WorkInfo.query.filter_by(zipcode=zipcode).all() if zipcode else WorkInfo.query.all()
    data = [{'name': w.name, 'address': w.address} for w in works]
    return jsonify(success=True, data={'works': data})

@bp.route('/api/workDetail/<name>', methods=['GET'])
@membership_required
def api_work_detail(name):
    info = WorkInfo.query.filter_by(name=name).first()
    if info:
        return jsonify(success=True, data={'name': info.name, 'address': info.address, 'content': info.content})
    else:
        return jsonify(success=False, message='未找到该公司'), 404