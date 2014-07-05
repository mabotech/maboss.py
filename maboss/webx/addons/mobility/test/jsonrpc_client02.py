# -*- coding: utf-8 -*- 

import time

import requests

"""

payload = {'signature':'165082e67e721b63529b73428d8f304152e3ecd3','timestamp':'b','nonce':'a','data':data2}

url = 'http://127.0.0.1:6226/mobi/weixin?echostr=echoabc&signature=165082e67e721b63529b73428d8f304152e3ecd3&timestamp=b&nonce=a'

#headers = {"Content-Type": "application/x-www-form-urlencoded"}

r = requests.post(url, data=data) #, headers=headers)


print r.headers['content-type']

print r.text

print r.url
"""

import json

payload = {"jsonrpc":"2.0","method":"Weixin.list","params":{"page":1, "limit":4, "orderby":"","sort_order":"DESC"},"id":"r1001"}

headers = {"content-type": "application/json"}

#r = requests.get('https://github.com/timeline.json')

url = "http://i.ngmes.net/"


r = requests.post(url, data=json.dumps(payload), headers=headers)
print url
print r.text

#print r