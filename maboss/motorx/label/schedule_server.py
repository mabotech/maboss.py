# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

from config import LOGGING_CFG_SCH, ENDPOINT

logging.config.fileConfig(LOGGING_CFG_SCH)

log = logging.getLogger(__name__)

import time

from time import strftime, localtime

import gevent

import zerorpc


from msgpack import packb, unpackb




def call_rpc(client, i, j):
    
    v =  client.lolita(i, j)
    
    log.debug("call rpc done")

def main():


    client = zerorpc.Client() #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT))
    
    client.connect(ENDPOINT) 
    
    i = 0
    
    while True:
        i = i + 1
        
        j = packb({'abc':i, 'func':'time'})
        
        t = time.time()
        
        try:
            
            #print strftime("%Y-%m-%d %H:%M:%S", localtime())            
            #call_rpc(client, i, j)
            
            # asyn call for no adjus timer
            log.debug('call_rpc')
            gevent.spawn(call_rpc, client, i, j )
            
            
        except Exception, e:
            'no heartbeat:restart the server / service'
            log.error( e.message )
            pass
            
        gevent.sleep(10)
    
        t2 = time.time()
        
        print t2-t


if __name__ == '__main__':
    
    main()    