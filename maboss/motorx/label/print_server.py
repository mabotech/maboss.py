
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

from config import LOGGING_CFG_SRV, ENDPOINT

logging.config.fileConfig(LOGGING_CFG_SRV)

log = logging.getLogger(__name__)

import time
from time import strftime, localtime

import gevent

import zerorpc

import random

from msgpack import packb, unpackb


from print_worker import PrintWorker


class LabelPrintServer(zerorpc.Server):
    
    def __init__(self):
        # initialize parent class
        super(LabelPrintServer, self).__init__()
        
        
    #    pw = PrintWorker()

    def lolita(self, i, j):
        
        v =  unpackb(j)
        
        log.debug(str(v))
        
        f = v['func']
        
        #print f
        
        if hasattr( self, f ):
            #print 'has'
            return self.__call__(f, i)
            
        
        return 42 + i + v['abc']
        
    def call_by_man(self, i, j):
        
        pass

    def time(self, i):
        #print strftime("%Y-%m-%d %H:%M:%S", localtime())
        
        #gevent.sleep(random.randint(0,5)*0.5)
        
        pw = PrintWorker()
        
        #it's already asyn mode when run in the server.
        #gevent.spawn(pw.printit).join()
        
        v = ""
        
        workstation = ""
        
        v = pw.printit(workstation)
        
        log.debug("printit:"+v)
        
        return str(i)+':%s' %(v)
        
        
def run():
    
    endpoint = ENDPOINT
    
    srv = LabelPrintServer()

    srv.bind(endpoint)

    log.info("running:" + endpoint)
    
    srv.run()
    
    
if __name__ == "__main__":

    run()