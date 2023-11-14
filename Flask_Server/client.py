import requests 
import json
import time

api = 'https://www.geek7.top:8091/callApi'

data = {
    'token' : time.time(),
    'channel':'tradplus_sdk_depends',
    'code':829,
    'channel':[''],
    'version':'',
    'region' : '2'
}

res = requests.get(api,) 
print(res.text)

