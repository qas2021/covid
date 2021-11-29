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

celery = Celery('app', broker='amqp://guest:guest@rabbitmq:5672//', include=['app.celery_task'])



@celery.task(bind=True, name="add")
def add(x,y):
    data = list()
    response = make_api_call(url = "https://covid-api.com/api/regions")
    for i in response['data']:
        country_obj = Country.from_json_body(i)
        logging.debug(country_obj.iso,"-----------------")
        stats_url = f"https://covid-api.com/api/reports?iso={country_obj.iso}"
        country_response = make_api_call(stats_url)
        Country.test(country_response,country_obj)
        logging.debug('<-->')
        models.db.session.commit()
        data.append(country_obj.to_json())
    return jsonify(data)