from flask import Flask
from flask_session import Session
import os

app = Flask(__name__)
# Ensuring .js files will not be cached
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
SESSION_TYPE = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config.from_object(__name__)
Session(app)

from music_fugitive.post.routes import post
from music_fugitive.main.routes import main

app.register_blueprint(post)
app.register_blueprint(main)
