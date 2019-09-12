from flask import Flask
from flask_session import Session
import os


def create_app():
    app = Flask(__name__)
    # Ensuring .js files will not be cached
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object(__name__)
    Session(app)
    register_blueprints(app)

    return app


def register_blueprints(app, url_prefix='/'):
    from music_fugitive.post.routes import post
    from music_fugitive.main.routes import main
    app.register_blueprint(post, url_prefix=url_prefix)
    app.register_blueprint(main, url_prefix=url_prefix)
