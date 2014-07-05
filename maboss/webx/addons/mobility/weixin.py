# -*- coding: utf-8 -*-

import sys

import re

#sys.path.append('c:/MTP/apps/database')

#from .error import InvalidUsage

import xml.etree.ElementTree as ET

from flask import Flask, Blueprint, current_app, request, render_template

from weixinlib import verification, process

from mabolab.core.base import Base

base = Base()
db = base.get_db('postgres') #'postgresql'  #default db is Oracle
log = base.get_logger()

settings = base.get_config()

TOKEN = settings['WEIXIN_TOKEN']

weixinapi =  Blueprint('weixinapi', __name__)

#homepage
@weixinapi.route('/')
def home():
    return render_template('index.html')
    #return "homepage"
#
@weixinapi.route('/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request, TOKEN) and echostr is not None:
        return echostr
    return 'access verification fail'

@weixinapi.route('/weixin', methods=['POST'])
def weixin_msg():
    
    log.debug( "post" )   
 
    log.debug(request.form)
    if verification(request, TOKEN):       
        
        data = request.data         
       
        msg = parse_msg(data)
        
        log.debug(msg)
     
        rmsg = process(msg)
        
        return rmsg

    return 'message processing fail'

def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg    