# -*- coding: utf-8 -*- 


import logging
import logging.handlers

#logging.config.fileConfig('c:/mtp/maboss0.1/configuration/logging.ini')

log = logging.getLogger(__name__)

import hashlib
import urllib, urllib2
import re
import time
import json

from mabolab.core.base import Base

base = Base()
db = base.get_db('postgresql') #'postgresql'  #default db is Oracle
log = base.get_logger()

settings = base.get_config()


from models.weixin import Weixin

class WeixinP(object):
    
    def __init__(self):
        pass
        
    def query(self):
        pass
        
        
    def create(self):
        pass
        
        
    

def get_response_xml2(info):
    
    msg = """<xml>
<ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
<FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
<CreateTime>%(CreateTime)s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%(information)s]]></Content>
</xml>""" % info
 
    return msg
    
#
#http://i.ngmes.net/img/news.png

def get_response_xml(info):
    
    msg = """ <xml>
<ToUserName><![CDATA[%(FromUserName)s]]></ToUserName>
<FromUserName><![CDATA[%(ToUserName)s]]></FromUserName>
<CreateTime>%(CreateTime)s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
 <ArticleCount>1</ArticleCount>
 <Articles>
 <item>
 <Title><![CDATA[%(information)s]]></Title> 
 <Description><![CDATA[description here]]></Description>
 <PicUrl><![CDATA[http://i.ngmes.net/img/news.png]]></PicUrl>
 <Url><![CDATA[http://www.mabotech.com]]></Url>
 </item>
 </Articles>
 </xml> """ % info
 
    return msg
    
    
def process(msg):    
    
    
    msgclass = '1'
    msgid = msg['MsgId']
    msgtype = msg['MsgType']
    fromusername = msg['FromUserName']
    tousername = msg['ToUserName']
    createtime=msg['CreateTime']
    content = msg['Content']
    createdby = 'MT'
    
    
    wx = Weixin(msgclass, msgid, msgtype, fromusername, tousername, createtime, content, createdby)
    
    try:
        
        db.session.add(wx)
        db.session.commit()
        
    except:
        db.session.rollback()      

    if user_subscribe_event(msg):
        return help_info(msg)
    elif is_text_msg(msg):
        content = msg['Content']
        kw = {}
        if content == u'?' or content == u'？':
            return help_info(msg)
        elif content[:4] == "早报":
            #kw = {}
            kw['information'] ='morning report'
            
            #rmsg = get_response_xml(kw)
            #return rmsg            
        elif content[:2] == "mt":
            kw['information'] = "report"
        else:
            #books = search_book(content)
            #rmsg = response_news_msg(msg, books)
            #kw = {}
            kw['information'] = '收到/got it'
        

        kw['FromUserName'] =fromusername # msg['FromUserName']
        kw['ToUserName'] = tousername
        kw['CreateTime'] = int(time.time())
        #kw['information'] = 'got it'
        
        rmsg = get_response_xml(kw)
        return rmsg

def verification(request, token):
    
    #args in url
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    #token = 'doumi' 
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    
    try:    
        tmpstr = ''.join(tmplist)
    except:
        return False
        
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    
    log.debug("hashstr:")
    log.debug(hashstr)
    #return True
    if hashstr == signature:
        return True
    return False




def is_text_msg(msg):
    return msg['MsgType'] == 'text'

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

HELP_INFO = \
u"""
欢迎关注MaboTech

直接关键字，即可提报和查询

如发送"日报"，将回复系统查询到的三条数据记录
"""

def help_info(msg):
    return response_text_msg(msg, HELP_INFO)

NEWS_MSG_HEADER_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<Content><![CDATA[]]></Content>
<ArticleCount>%d</ArticleCount>
<Articles>
"""

NEWS_MSG_TAIL = \
u"""
</Articles>
<FuncFlag>1</FuncFlag>
</xml>
"""

#消息回复，采用news图文消息格式
def response_news_msg(recvmsg, data):
    msgHeader = NEWS_MSG_HEADER_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'], 
        str(int(time.time())), len(data))
    msg = ''
    msg += msgHeader
    msg += make_articles(data)
    msg += NEWS_MSG_TAIL
    return msg

def make_articles(data):
    msg = ''
    if len(data) == 1:
        msg += make_single_item(data[0])
    else:
        for i, book in enumerate(data):
            msg += make_item(data, i+1)
    return msg

NEWS_MSG_ITEM_TPL = \
u"""
<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
</item>
"""

def make_item(data, itemindex):
    title = u'%s\t%s分\n%s\n%s\t%s' % (data['title'], data['rating']['average'], 
        ','.join(data['author']), data['publisher'], data['price'])
    description = ''
    picUrl = data['images']['large'] if itemindex == 1 else data['images']['small']
    url = data['alt']
    item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
    return item

#图文格式消息只有单独一条时，可以显示更多的description信息，所以单独处理
def make_single_item(data):
    title = u'%s\t%s分' % (data['title'], data['rating']['average'])
    description = '%s\n%s\t%s' % (','.join(data['author']), data['publisher'], data['price'])
    picUrl = data['images']['large']
    url = data['alt']
    item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
    return item

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], 
        str(int(time.time())), content)
    return s
