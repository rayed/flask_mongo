import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bson.objectid import ObjectId

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.cli.command('fake_seed')
def fake_seed():
    from faker import Faker
    fake = Faker()
    db = get_db()
    collection = db["posts"]
    for i in range(100):
        data = {
                "title": fake.sentence(),
                "body": "\n".join(fake.paragraphs()),
        }
        collection.insert_one(data)
    print("done")




@bp.route('/')
def index():
    db = get_db()
    collection = db["posts"]
    posts = collection.find()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            data = {
                    "title":title,
                    "body": body,
            }
            db = get_db()
            collection = db["posts"]
            collection.insert_one(data)
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    collection = db["posts"]
    post = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            query = {'_id': ObjectId(id)}
            data = {
                "$set": {
                    "title":title,
                    "body": body,
                } 
            }
            collection.update_one(query, data)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    collection = db["posts"]
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('blog.index'))
