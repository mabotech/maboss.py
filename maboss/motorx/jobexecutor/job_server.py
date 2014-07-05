
# -*- coding: utf-8 -*-

import sys

from config import CENTRAL_CONFIG
#from config import LOGGING_CFG_SRV, ENDPOINT

#logging.config.fileConfig(LOGGING_CFG_SRV)

if 'threading' in sys.modules:
        raise Exception('threading module loaded before patching!')
        
from gevent import monkey
# patch_all
monkey.patch_all()

from flask.config import Config

settings = Config("")

settings.from_pyfile(CENTRAL_CONFIG)

settings['APP_NAME'] = "jobexecutor"

import logging
import logging.handlers
import logging.config

from mabolab.core.base import Base

base = Base(settings)
db = base.get_db()
log = base.get_logger()

pf_log = logging.getLogger('performance')

import time
from time import strftime, localtime

import gevent
from gevent import Timeout

import zerorpc

import random

from msgpack import packb, unpackb

from mabolab.executor import py_executor
#from print_worker import PrintWorker


class JobExecutorServer(zerorpc.Server):
    
    def __init__(self, heartbeat, pool_size):
        
        # initialize parent class
        super(JobExecutorServer, self).__init__(heartbeat=heartbeat, pool_size=pool_size)
        
    def time(self):
        
        return  time.time()

    def execute(self, name, args, func_type='PY'):        

        module_path = settings['MODULE_PATH'] #"c:/mtp/mabotech/maboss1.1"
        
        info = "[%s]%s:%s" % (module_path, func_type, name)
        log.debug( info)
        
        t = time.time()
        
        if name == "time":
            #for reconnection testing
            return t
        
        #Sync Code Here !!!
        
        timeout = Timeout(5, Exception)
        timeout.start()
        try:
            #...  # exception will be raised here, after *seconds* passed since start() call
            rtn = "OK"
            rtn = py_executor.execute(name, args, module_path) 
            #gevent.sleep(0.02)
            pf_log.debug("%10.5f,%s,%s" %(time.time()-t, func_type, name ) )
            
            return rtn                    
        except Exception, e:
            log.error(e.message)
            #log.debug("timeout!")
        finally:
            timeout.cancel()
            
            #raise Exception("Timeout")

        
def run():
    
    endpoint = settings['ENDPOINT_JOBEXECUTOR']
    
    srv = JobExecutorServer(heartbeat=2, pool_size=10)

    srv.bind(endpoint)

    log.info("running:" + endpoint)
    
    srv.run()
    
def stop():
    endpoint = settings['ENDPOINT_JOBEXECUTOR']
    log.info("stopping:"+ endpoint)
    
if __name__ == "__main__":

    run()