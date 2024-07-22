from flask import render_template, request, Blueprint
from . import utils

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/result', methods=['POST'])
def result():
    zipcode = request.form['zipcode']
    info = utils.get_info_by_zipcode(zipcode)
    return render_template('result.html', info=info)
