from app import app
import requests
import json
from app.models import Country
from app import models
def country_data(iso):
    return 0
global serial
@app.route('/', methods=['GET'])

def get_data():
    serial = 1
    url = "https://covid-api.com/api/regions"
    iso = []
    country = []
    page = ''
    while page == '':
        try:
            page = requests.get(url, timeout= 10)
            break
        except:
            print("Connection refused by the server..")
            continue
    # page = page.decode("utf-8")
    data=''
    for a in page:
        a=a.decode("utf-8")
        data = data + a
    dctn = json.loads(data)
    # print(type(dctn))
    # print(dctn)
    serial = 1
    for a in dctn:
        for i in dctn[a]:
            for key, value in i.items():
                if key == 'iso':
                    iso.append(value)
                if key == 'name':
                    country.append(value)
    for i,j in zip(country,iso):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", i, j)
        insert = Country(j,i,serial)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        urld="https://covid-api.com/api/reports?iso={}".format(j)
        pagee = ''
        while pagee == '':
            try:
                pagee = requests.get(urld, timeout= 10)
                break
            except:
                print("Connection for iso refused by the server..")
                continue
        temp= models.Country.test(pagee,serial,insert)
        models.db.session.add(insert)
        models.db.session.commit()
        serial = temp + 1

    # insert = Country('USA',"abc",serial)
    # urld="https://covid-api.com/api/reports?iso={}".format('USA')
    # pagee = ''
    # while pagee == '':
    #     try:
    #         pagee = requests.get(urld, timeout= 10)
    #         break
    #     except:
    #         print("Connection for iso refused by the server..")
    #         continue
    # temp= models.Country.test(pagee,serial,insert)
    # serial =temp
    # models.db.session.add(insert)
    # models.db.session.commit()
    
    # print(models.country.query.filter_by(iso='USA').first().id)
    




    # for i in iso:
    #     urld="https://covid-api.com/api/reports?iso={}".format(i)
    #     pagee = ''
    #     while pagee == '':
    #         try:
    #             pagee = requests.get(urld, timeout= 10)
    #             break
    #         except:
    #             print("Connection for iso refused by the server..")
    #             continue

    #     temp=models.stats.test(pagee,serial)
    #     serial=temp
    return pagee.content

@app.route('/report', methods=['GET'])
def data():
    import requests
    import json
    url = "https://thevirustracker.com/free-api?global=stats"
    iso = []
    country = []
    page = ''
    while page == '':
        try:
            page = requests.get(url, timeout= 500)
            break
        except:
            print("Connection refused by the server..")
            continue
    # page = page.decode("utf-8")
    data=''
    for a in page:
        a=a.decode("utf-8")
        data = data + a
    dctn = json.loads(data)
    print(type(dctn))
    print(dctn)
