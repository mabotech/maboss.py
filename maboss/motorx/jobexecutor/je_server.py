
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

        module_path = settings['MODULE_PATH'] #"c:/mtp/mabotech/maboss1.1"
        
        info = "[%s]%s:%s" % (module_path, func_type, name)
        log.debug( info)
        
        t = time.time()
        rtn = py_executor.execute(name, args, module_path) 
        
        pf_log.debug("%10.5f,%s,%s" %(time.time()-t, func_type, name ) )
        
        return rtn   


        
        
def run():
    
    endpoint = settings['ENDPOINT_JOBEXECUTOR']
    
    srv = JobExecutorServer()

    srv.bind(endpoint)

    log.info("running:" + endpoint)
    
    srv.run()
    
    
if __name__ == "__main__":

    run()