from flask import Blueprint, render_template

bp = Blueprint('common', __name__)


@bp.route('/about')
def about():
    return render_template('common/about.html')
