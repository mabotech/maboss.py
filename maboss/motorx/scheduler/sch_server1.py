# -*- coding: utf-8 -*-


from config import LOGGING_CFG_SCH, ENDPOINT

import logging
import logging.handlers
import logging.config

if __name__ == "__main__":
    from mabolab.database.config import LOGGING
    logging.config.dictConfig( LOGGING )

log = logging.getLogger(__name__)

import time

from time import strftime, localtime

import gevent

import zerorpc


from msgpack import packb, unpackb




def call_rpc(client, name, args):
    
    rtn =  client.execute(name, args)
    
    log.debug("call rpc done [%s]" %(rtn) )

def main():


    client = zerorpc.Client() #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT))
    
    client.connect(ENDPOINT) 
    
    i = 0
    
    module_path = "c:/mtp/mabotech/maboss1.1"
    
    name = "label2.print_label"
    
    while True:
        
        i = i + 1
        
        args = packb({'workstation':62300, 'fields':{'SN':'SN002'}})
        
        t = time.time()
        
        try:
            
            #print strftime("%Y-%m-%d %H:%M:%S", localtime())            
            #call_rpc(client, i, j)
            
            # asyn call for no adjus timer
            log.debug('call_rpc')
            
            gevent.spawn(call_rpc, client, name, args)
            
            
        except Exception, e:
            'no heartbeat:restart the server / service'
            log.error( e.message )
            pass
            
        gevent.sleep(10)
    
        t2 = time.time()
        
        print t2-t


if __name__ == '__main__':
    
    main()    