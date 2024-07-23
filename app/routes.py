from flask import render_template, request, Blueprint, abort
from . import utils

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/result', methods=['POST'])
def result():
    zipcode = request.form['zipcode']
    addresses = utils.get_addresses_by_zipcode(zipcode)
    return render_template('result.html', zipcode=zipcode, addresses=addresses)

@bp.route('/detail/<address>')
def detail(address):
    info = utils.get_info_by_address(address)
    if info:
        return render_template('detail.html', info=info)
    else:
        abort(404)

@bp.route('/contact')
def about():
    return render_template('contact.html')