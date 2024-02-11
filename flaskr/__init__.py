import os
import re
from flask import Flask
import re
from jinja2 import pass_eval_context
from markupsafe import Markup, escape

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

    # Source: https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters
    @app.template_filter('nl2br')
    @pass_eval_context
    def nl2br(eval_ctx, value):
        br = "<br>\n"
        if eval_ctx.autoescape:
            value = escape(value)
            br = Markup(br)
        result = "\n\n".join(
            f"<p>{br.join(p.splitlines())}</p>"
            for p in re.split(r"(?:\r\n|\r(?!\n)|\n){2,}", value)
        )
        return Markup(result) if eval_ctx.autoescape else result
    
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
