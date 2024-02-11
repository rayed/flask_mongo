import click
from flask import Blueprint, render_template
from bson.objectid import ObjectId

from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    collection = db["posts"]
    posts = collection.find()
    return render_template('blog/index.html', posts=posts)


@bp.route('/blog/<id>')
def view(id):
    db = get_db()
    collection = db["posts"]
    post = collection.find_one({'_id': ObjectId(id)})
    return render_template('blog/view.html', post=post)
