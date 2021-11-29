import datetime
import jwt
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from functools import wraps
from celery import Celery
from marshmallow import fields
import pymysql
import requests
import time
import json 
from flask_sqlalchemy import SQLAlchemy
import configparser
from flask import jsonify, request
from .requestapi import make_api_call
config_obj = configparser.ConfigParser()
config_obj.read('configfile.ini')
dbparam = config_obj['sqlalchemy']


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qasim:Qwer_1234-@localhost/lostnfound'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(dbparam['user'],dbparam['password'],dbparam['host'],dbparam['database'])

# simple_app = Celery('workers',
#                     broker='amqp://guest:guest@rabbit:5672')

db = SQLAlchemy(app)
from app import models
from app import views
models.db.create_all()