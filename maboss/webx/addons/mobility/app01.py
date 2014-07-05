#!/bin/env python
# -*- coding: utf-8 -*- 


import logging
import logging.handlers
import logging.config

logging.config.fileConfig('logging.ini')

log = logging.getLogger(__name__)

import xml.etree.ElementTree as ET

from flask import Flask, request, render_template
from private_const import APP_SECRET_KEY, DOUBAN_APIKEY

from weixin import verification, process

app = Flask(__name__)
#app.debug = True
#app.secret_key = APP_SECRET_KEY

#homepage just for fun
@app.route('/webi/')
def home():
    return render_template('index.html')

#公众号消息服务器网址接入验证
#需要在公众帐号管理台手动提交, 验证后方可接收微信服务器的消息推送
@app.route('/webi/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

#来自微信服务器的消息推送
@app.route('/webi/weixin', methods=['POST'])
def weixin_msg():
    
    log.debug( "post" )   
 
    log.debug(request.form)
    if verification(request):       
        
        data = request.data         
       
        msg = parse_msg(data)       
     
        rmsg = process(msg)
        
        return rmsg

    return 'message processing fail'

def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg    


if __name__ == '__main__':
    
    #app.debug = True
    
    app.run(port=5080, debug = True)
