import sys
from getpass import getpass
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import click
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('admin_users', __name__, url_prefix='/admin/users')


@bp.cli.command('create')
@click.argument('username')
def create(username):
    db = get_db()
    collection = db["users"]
    user = collection.find_one({'username': username})
    if user is not None:
        print("User already exists")
        sys.exit(1)
    password = getpass()
    data = {
            "username": username,
            "password": generate_password_hash(password),
    }
    collection.insert_one(data)
    print(f"user \"{username}\" created")


@bp.cli.command('reset')
@click.argument('username')
def reset(username):
    db = get_db()
    collection = db["users"]
    user = collection.find_one({'username': username})
    if user is None:
        print("User does not exist")
        sys.exit(1)
    password = getpass()
    query = {'username': username}
    data = {
        "$set": {
            "username":username,
            "password": generate_password_hash(password),
        } 
    }
    collection.update_one(query, data)
    print(f"user \"{username}\" password changed")


@bp.route('/')
def index():
    db = get_db()
    collection = db["users"]
    users = collection.find()
    return render_template('admin/users/index.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            data = {
                    "username": username,
                    "password": generate_password_hash(password),
            }
            db = get_db()
            collection = db["users"]
            collection.insert_one(data)
            return redirect(url_for('admin_users.index'))

    return render_template('admin/users/create.html')


@bp.route('/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    collection = db["users"]
    user = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            query = {'_id': ObjectId(id)}
            data = {
                "$set": {
                    "username":username,
                    "password": generate_password_hash(password),
                } 
            }
            collection.update_one(query, data)
            return redirect(url_for('admin_users.index'))

    return render_template('admin/users/update.html', user=user)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    collection = db["users"]
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('admin_users.index'))
