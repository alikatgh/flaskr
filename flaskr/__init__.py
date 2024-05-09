import os
import click
from flask import Flask
from flask_login import LoginManager

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # Define the init-db command
    @app.cli.command('init-db')
    def init_db_command():
        """Clear the existing data and create new tables."""
        db.init_db()
        click.echo('Initialized the database.')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        if user:
            return User(user['id'], user['username'], user['password'])
        return None

    return app

class User:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)