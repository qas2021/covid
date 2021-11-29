from os import name
from celery import Celery
from celery.result import AsyncResult
from app import app
from app.models import Country
from app import models
from flask import jsonify, request
from .requestapi import make_api_call
import logging
# from celery.utils.log import get_task_logger

# logger = get_task_logger(__name__)

celery = Celery('app', broker='amqp://guest:guest@rabbitmq:5672//', include=['app.celery_app'])



@celery.task(bind=True, name="add")
def add(x,y):
    logging.debug("A"*100)
    print("b"*300)
    return "hello"