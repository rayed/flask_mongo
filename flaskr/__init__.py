import os

from flask import Flask
from . import common
from . import auth
from . import admin_users
from . import blog
from . import admin_blog
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.register_blueprint(common.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin_users.bp)
    app.register_blueprint(admin_blog.bp)
    app.register_blueprint(blog.bp)

    @app.template_filter('nl2br')
    def nl2br(s):
        return "\n".join(["<p>"+line+"</p>" for line in s.split("\n") if line.strip() != ""])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
