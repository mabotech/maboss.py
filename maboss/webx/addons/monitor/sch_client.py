# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

if __name__ == "__main__":
    from mabolab.database.config import LOGGING
    logging.config.dictConfig( LOGGING )

log = logging.getLogger(__name__)

import time

from time import strftime, localtime

from flask import Flask, Blueprint, current_app, jsonify, request

import gevent

import zerorpc

from msgpack import packb, unpackb

from mabolab.core.base import Base

#base = Base()

#settings = base.get_config()
#settings['ENDPOINT_JOBEXECUTOR_REQ']  # 
ENDPOINT_REQ = "tcp://127.0.0.1:62002"

#log = base.get_logger()

def start_job(jobid):
    sch_man(jobid, "add_job")
    
def stop_job(jobid):
    sch_man(jobid, "stop_job")
    
def get_status():
    
    name = "query"
    
    client = zerorpc.Client(heartbeat=1) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    #module_path = "c:/mtp/mabotech/maboss1.1"
    
    #name = "add_job"
    #name = "stop_job"
    log.debug("service:%s"%(name))
    
    args = {"id":0}
    
    args = packb(args)
    v = 'init'
    try:
        v =  client.execute(name, args)
        log.debug( v )
    except zerorpc.exceptions.LostRemote, e:
        v = "exception:"+e.message
        log.debug(e.message)
    
    client.close()   
    
    return v
    
    
def sch_man(jid, name): 
    
    sn = ""#request.args.get('sn', 'SN0123')

    """
    print_manually
    """
    
    #default heartbeat = 5, so if server is down raise: zerorpc.exceptions.LostRemote: Lost remote after 10s heartbeat
    client = zerorpc.Client(heartbeat=1) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    #module_path = "c:/mtp/mabotech/maboss1.1"
    
    #name = "add_job"
    #name = "stop_job"
    log.debug("service:%s"%(name))
    
    args = {"id":jid,"name":"label2.print_label_sch","args": {"workstation":"62300"},"interval": 10, "active": 1, "last_run_on":None}
    
    args = packb(args)
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
    
    #for i in range(10, 100):
    #start_job(1)
    
    stop_job(1)
    
    get_status()