from flask import render_template, request, Blueprint, abort
from . import utils

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/rent')
def rent():
    return render_template('rent.html')

@bp.route('/rentBlack')
def rentBlack():
    return render_template('rentBlack.html')

@bp.route('/rentResult', methods=['POST'])
def rentResult():
    zipcode = request.form['zipcode']
    addresses = utils.get_addresses_rent(zipcode)
    return render_template('rentResult.html', zipcode=zipcode, addresses=addresses)

@bp.route('/rentDetail/<address>')
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