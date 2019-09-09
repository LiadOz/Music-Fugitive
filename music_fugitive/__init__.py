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

import music_fugitive.views
