# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask import Flask
from flask_bootstrap import Bootstrap
app = Flask(__name__, static_url_path='/static')

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

bs = Bootstrap(app) #flask-bootstrap

from app import video_analyser_controller
from os.path import expanduser

UPLOAD_FOLDER = expanduser("~") + "/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
