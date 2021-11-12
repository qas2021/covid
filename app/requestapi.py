import requests
import json

def make_api_call(url):
    page = ''
    while page == '':
        try:
            page = requests.get(url, timeout= 10)
        except:
            print("Connection refused by the server..")

    data=''
    for a in page:
        a=a.decode("utf-8")
        data = data + a

    response = json.loads(data)
    return response
