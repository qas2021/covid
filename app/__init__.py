import datetime
import jwt
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from functools import wraps
import re
from marshmallow import fields
import pymysql
import requests
import time
import json 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qasim:Qwer_1234-@localhost/covid'
db = SQLAlchemy(app)
from app import models
from app import views
models.db.create_all()