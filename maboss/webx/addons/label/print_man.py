# -*- coding: utf-8 -*-

import time

from time import strftime, localtime

from flask import Flask, Blueprint, current_app, jsonify, request

import gevent

import zerorpc

from msgpack import packb, unpackb

from mabolab.core.base import Base

base = Base()

settings = base.get_config()

ENDPOINT_REQ = settings['ENDPOINT_JOBEXECUTOR_REQ']  # "tcp://127.0.0.1:62001"

log = base.get_logger()


def print_man(): 
    
    sn = request.args.get('sn', 'SN0123')

    """
    print_manually
    """
    
    #default heartbeat = 5, so if server is down raise: zerorpc.exceptions.LostRemote: Lost remote after 10s heartbeat
    client = zerorpc.Client(heartbeat=1) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    #module_path = "c:/mtp/mabotech/maboss1.1"
    
    name = "label2.print_label"
    log.debug("service:%s"%(name))
    args = packb({'workstation':62300, 'fields':{'SN':sn}})
    v = 'init'
    try:
        v =  client.execute(name, args)
        log.debug( v )
    except zerorpc.exceptions.LostRemote, e:
        v = "exception:"+e.message
        log.debug(e.message)
    
    client.close()   
    
    return v
    
if __name__ == '__main__':
    
    print_man()
    