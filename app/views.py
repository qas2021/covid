from app import app,db
from app.models import Country, Province, ProvinceStat , City, CityStat
from app import models,DataDict
from flask import jsonify, request
from .requestapi import make_api_call
import logging
# from .utils import make_api_call
logging.basicConfig(level= logging.DEBUG)

@app.route('/', methods=['GET'])
def get_data():
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
    # country_obj = Country.from_json_body(response['data'][2])
    # stats_url = f"https://covid-api.com/api/reports?iso={country_obj.iso}"
    # country_response = make_api_call(stats_url)
    # Country.test(country_response,country_obj)
    # models.db.session.commit()
    # data = Country.to_json()
    # data =  
    return jsonify(data)

@app.route('/searchcountry', methods = ['POST'])
def search():
    data= ''
    iso = request.form['iso']
    data = Country.search_json(iso)
    return jsonify(data)


