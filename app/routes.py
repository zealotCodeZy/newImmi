from flask import render_template, request, Blueprint, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from . import utils
from functools import wraps

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
    addresses = utils.get_addresses_rent(zipcode)
    return render_template('rentResult.html', zipcode=zipcode, addresses=addresses)

@bp.route('/rentDetail/<address>')
@login_required
@membership_required
def rentDetail(address):
    info = utils.get_info_rent(address)
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
    names = utils.get_name_work(name)
    return render_template('workResult.html', name=name, names=names)

@bp.route('/workDetail/<name>')
def workDetail(name):
    info = utils.get_info_work(name)
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