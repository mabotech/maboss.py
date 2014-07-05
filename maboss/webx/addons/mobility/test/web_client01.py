# -*- coding: utf-8 -*- 

import time

import requests


msg = ["早报信息", "晚报信息","日报20130102" ,"日报"]


for m in msg:
    #print len(m)
    #print m[:4]
    pass



r = requests.get('http://127.0.0.1:6226/api/weixin?echostr=echoabc&signature=165082e67e721b63529b73428d8f304152e3ecd3&timestamp=b&nonce=a')

#print dir(r)

print r.headers['content-type']

print r.text

print '=='*20

#print dir(requests)

#url = 'http://127.0.0.1:5080/webi/weixin'

data = '''<xml>
 <ToUserName><![CDATA[maboss]]></ToUserName>
 <FromUserName><![CDATA[user_name1]]></FromUserName> 
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 <MsgId>%s</MsgId>
 </xml>''' %(int(time.time()), msg[0], int(time.time()))
 
#print data

data2 = """<xml><ToUserName><![CDATA[user003]]></ToUserName>
<FromUserName><![CDATA[MaboTech]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[subscribe]]></Event>
<EventKey><![CDATA[EVENTKEY]]></EventKey>
</xml>""" % (time.time())


payload = {'signature':'165082e67e721b63529b73428d8f304152e3ecd3','timestamp':'b','nonce':'a','data':data2}

url = 'http://127.0.0.1:6226/api/weixin?echostr=echoabc&signature=165082e67e721b63529b73428d8f304152e3ecd3&timestamp=b&nonce=a'


#headers = {"Content-Type": "application/x-www-form-urlencoded"}

r = requests.post(url, data=data) #, headers=headers)


print r.headers['content-type']

print r.text

print r.url