from flask import Flask, session
from flask.ext.session import Session

app = Flask(__name__)
# Check Configuration section for more details

# DEBUG = False
# SECRET_KEY = 'RED PANDA'
# # DATABASE_URI = 'sqlite:////tmp/database.db
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)

ALLOWED_EXTENSIONS = set(['json'])

