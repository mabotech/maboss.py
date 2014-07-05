
# -*- coding: utf-8 -*-

import sys

import logging
import logging.handlers
import logging.config


from config import CENTRAL_CONFIG
#from config import LOGGING_CFG_SRV, ENDPOINT

#logging.config.fileConfig(LOGGING_CFG_SRV)

#log = logging.getLogger(__name__)

import time
from time import strftime, localtime

import gevent

import zerorpc

import random

from msgpack import packb, unpackb

from mabolab.executor import py_executor
#from print_worker import PrintWorker


class JobExecutorServer(zerorpc.Server):
    
    def __init__(self):
        
        # initialize parent class
        super(JobExecutorServer, self).__init__()

    def execute(self, name, args, func_type='PY'):        

        module_path = "c:/mtp/mabotech/maboss1.1"

        log.debug("[%s]%s:%s" % (module_path, func_type, name) )
        
        rtn = py_executor.execute(name, args, module_path) 
        
        return rtn   


        
        
def run():
    
    endpoint = ENDPOINT
    
    srv = JobExecutorServer()

    srv.bind(endpoint)

    log.info("running:" + endpoint)
    
    srv.run()
    
    
if __name__ == "__main__":

    run()