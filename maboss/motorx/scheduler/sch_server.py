# -*- coding: utf-8 -*-

import os, sys

from config import CENTRAL_CONFIG

if 'threading' in sys.modules:
        raise Exception('threading module loaded before patching!')

      
from gevent import monkey
# patch_all
monkey.patch_all()


from flask.config import Config

settings = Config("")

settings.from_pyfile(CENTRAL_CONFIG)

settings['APP_NAME'] = "scheduler"

from mabolab.core.base import Base

base = Base(settings)
db = base.get_db()
log = base.get_logger()

import time

from time import strftime, localtime

import gevent

import zerorpc

import simplejson as json

from msgpack import packb, unpackb

from job_info import JobInfo

from mabolab.common.singleton import Singleton

class Connector(Singleton):
    
    def __init__(self):
        
        self.endpoint = settings['ENDPOINT_JOBEXECUTOR_REQ']

        self.client = zerorpc.Client(timeout=3, heartbeat=1) #heartbeat=None
    
        log.info("client connect: %s" % (self.endpoint))
        
        self.client.connect(self.endpoint) 
        
        self.lock = 0
        
        self.status = 0
        
        self.errors = 0
    
    def get_client(self):
        
        return self.client
        
    def reconnect(self):
        
        if self.lock == 1:
            log.warning("locked...")
            gevent.sleep(1)
            return None
            
        else:
            self.lock = 1
            log.warning("reconnect...")
            
            #self.client.close()
            

            self.client.connect(self.endpoint)
            try:
                rtn = self.client.execute("time", "")
                log.debug( "=================TEST:%s ===================" % (rtn) )
                self.errors = 0
            except Exception, e:
                log.error("reconnection failed:%s" %(e.message))
                pass
                
            self.lock = 0
            
            #return self.client

def reconnect(client):
    
    endpoint = settings['ENDPOINT_JOBEXECUTOR_REQ']
    
    log.info("client connect: %s" % (endpoint))
    
    client.connect(endpoint)  
    

def call_rpc(name, args):
    
    
    connector  = Connector()
    
    client = connector.get_client()
    #print dir(client)
    
    log.debug("ERROR TIMES: %s " % (connector.errors) )
    try:
        
        #if connector.errors > 10:
        #    raise Exception("connection failed")
            
        log.debug(">>>>call rpc:%s" %(name) )
        rtn =  client.execute(name, args)
        log.debug("<<<<call rpc done [%s]" %(unpackb(rtn)) )
        
        connector.status = 1
        connector.errors = 0
    except Exception, e: 
        
        connector.errors = connector.errors +1
        del connector
        log.debug("!!"*40)        
        log.error(e.message)
        #connector.reconnect()
    

def loop(jobid):
    
    jobinfo = JobInfo()
    
    i = 0
    
    module_path = settings['MODULE_PATH'] #"c:/mtp/mabotech/maboss1.1"
    
    name = jobinfo.jobs[jobid]['name'] #"label2.print_label"
    
    interval = jobinfo.jobs[jobid]['interval']
    
    while True:
        
        log.debug("="*10+str(jobid)+"="*10)
        #log.debug(jobid)
 
        if jobid not in jobinfo.jobs or  jobinfo.jobs[jobid]['active'] == 0:
            log.warning('quit loop:%s,%s' %(jobid, name) )
            break
            
        try:
            args = json.loads( jobinfo.jobs[jobid]['args'] )
            log.debug(args)
        except Exception,e:
            log.debug("$$"*20)
            log.error(e.message)
            return
        
      
        i = i + 1
        
        #args = packb({'workstation':62300, 'fields':{'SN':'SCH002%s' % (jobid) }})
        
        t = time.time()
        
        try:
            
            #print strftime("%Y-%m-%d %H:%M:%S", localtime())            
            #call_rpc(client, i, j)
            
            # asyn call for no adjus timer
            log.debug('[%s]call_rpc:%s' % (jobid, name))
            
            gevent.spawn(call_rpc, name, packb(args))
            
            
        except Exception, e:
            'no heartbeat:restart the server / service'
            log.error( e.message )
            pass
            
        gevent.sleep(interval)
    
        t2 = time.time()
        
        #print t2-t
        

def run1():
    
    for i in xrange(2):
        gevent.spawn(main, i)
    gevent.sleep(100)
    
class SchedulerServer(zerorpc.Server):
    
    def __init__(self):
        
        # initialize parent class
        super(SchedulerServer, self).__init__()
        #self.client = client
        self.jobinfo  = JobInfo()
        
        self.threads = {}
        
    def check_thread(self, jobid):
        
        if jobid in self.threads:
            if self.threads[jobid].dead == True:
                del self.threads[jobid]
            else:
                return False        
        return True
        
    def add_thread(self, jobid, thread):
        log.warning("starting new job:[%s]" % (jobid) )
        self.threads[jobid] = thread
        
    def stop_thread(self, jobid):
        
        self.threads[jobid].kill()
        
        del self.threads[jobid]
        log.warning("job[%s] was killed" % (jobid) )

    def execute(self, name, args):        

        #module_path = settings['MODULE_PATH'] #"c:/mtp/mabotech/maboss1.1"
        
        #info = "[%s]%s:%s" % (module_path, func_type, name)
        #log.debug( info)
        
        t = time.time()
        #rtn = py_executor.execute(name, args, module_path) 
        rtn = 'ok'
        #pf_log.debug("%10.5f,%s,%s" %(time.time()-t, func_type, name ) )
        args = unpackb(args)
        jobid = args['id']
        if name == "add_job":            
            
            args['last_run_on'] = None          
            
            del args['id']
            
            args['args'] = json.dumps(args['args'])
        
            self.jobinfo.add_job(jobid, args)
            
            #print self.jobinfo.jobs
            s = self.check_thread(jobid)
            if s == True:
                thread = gevent.spawn(loop, jobid)
                self.add_thread(jobid, thread)
            else:
                log.warning("can't add the running job:[%s]" %(jobid))
            #print self.threads
            
        elif name == "stop_job":
            
            if jobid in self.threads:
                self.stop_thread(jobid)
                self.jobinfo.del_job(jobid)
                
                #del self.threads[jobid]
                
                #print self.threads
            else:
                log.warning("no this job running:[%s]" % (jobid) )
                pass
        
        elif name == "query":
            
            data = []
            
            for key in self.jobinfo.jobs.keys():
                
                v = self.jobinfo.jobs[key]
                
                v['id'] = key
                
                data.append(v)
            
            return data
            
            
        return rtn        
        
def run():
    
    jobinfo = JobInfo()
    
    #client = zerorpc.Client(heartbeat=1) #heartbeat=None
    
    #endpoint = settings['ENDPOINT_JOBEXECUTOR_REQ']
    
    #log.info("client connect: %s" % (endpoint))
    
    #client.connect(endpoint)     
    
    fn = settings['CRON_CONF']#"cron.csv"
    
    log.info(fn)
    
    jobinfo.load(fn)
    
    log.debug( jobinfo.jobs )   
    
    endpoint = settings['ENDPOINT_SCHEDULER']
    
    srv = SchedulerServer()

    log.info("running:" + endpoint)
    
    srv.bind(endpoint)


    
    #run active job
    for jobid in jobinfo.jobs:
        log.debug("=="*30)
        log.debug(jobid)
        thread = gevent.spawn(loop, jobid)    
        srv.add_thread(jobid, thread)
    
    srv.run()
    
def stop():
    endpoint = settings['ENDPOINT_JOBEXECUTOR']
    log.info("stopping:"+ endpoint)    

if __name__ == '__main__':   
    
    run()    
    
    