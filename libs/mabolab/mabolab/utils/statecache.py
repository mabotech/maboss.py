# -*- coding: UTF-8 -*-

import time

from twisted.internet import threads, reactor

from turbomail import Message
from turbomail.control import interface
from time import strftime, localtime

import memcache

import traceback

import logging
import logging.handlers, logging.config

log= logging.getLogger('memcached')

class Singleton(type):
  def __call__(cls, *args):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__call__(*args)
    return cls.instance


class MCClient:
  
    __metaclass__ = Singleton
  
    def __init__(self):
        try:
            self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            #self.mc = None
            pass
        except:
            raise Exception("can't create Memcached Client")
    
    def reinit(self):
        try:
            log.debug( "reinit...")
            self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        except:
            raise Exception("can't create Memcached Client")
            
    def get(self, key):
        try:
            v = self.mc.get(key)
            #print "v",v
            #if v == None:
            #self.init()
            return v
        except Exception, e:
            print e, key
            #self.reinit()
            return None
        
    def set(self, key, value):
        try:
            return self.mc.set(key, value)
        except:
            #self.reinit()
            print key
            return None
        
    def get_stats(self):
        try:
            return self.mc.get_stats()
        except:
            return None
        
    def delete(self, key):
        try:
            return self.mc.delete(key)
        except:
            return None
    
class Sendmail:

    def __init__(self):

        self.turbomail_config = {
            'mail.on': True,
            'mail.transport': 'smtp',
            'mail.smtp.server': 'mailrelay.cummins.com',
            #'mail.smtp.username':'jianjun.ma@cummins.com',
            #'mail.smtp.password':'xxxxxx',
            #'mail.smtp.debug': True,
            'mail.utf8qp.on': True,
            'mail.auth':False,

            #'mail.smtp.tls':True,
        }



    def send(self, mfrom, mto, subject, html_part):

        interface.start(self.turbomail_config)

        message = Message(mfrom, mto, subject=subject)
        #message.cc =('idea','idea@mabotech.com')
        message.encoding = 'gb2312'
        message.plain = "Mabotech"
        message.rich = html_part
        message.send()

        interface.stop()


    def stop(self):
        pass    
    
class StateCache:
  
    def __init__(self, device, current_state = '0'):
        
        self.device = device
        
        self.HBThreshold = 15
        
        self.ReportInterval = 300
    
        self.mcclient = MCClient()
        
        #self.mcclient.init()
        
        #self.mc = self.client.mc
        
        self.tagLastState = '%s.LastState' %(device)
        
        self.tagCurrentState = '%s.CurrentState' %(device)
        
        self.tagMessage = '%s.Message' %(device)
        
        self.tagLastReportOn = '%s.LastReportOn' %(device)
        
        self.tagLastUpdateOn = '%s.LastUpdateOn' %(device)
        
        self.tagHeartBeat = '%s.LastHeartBeatOn' %(device)
        
        self.tagInit()
        
        log.debug("Cached Init: %s"%(device))
    
    def tagInit(self, current_state='0'):
        
        if self.mcclient.get(self.tagLastReportOn) == None:
            self.mcclient.set(self.tagLastReportOn, time.time())

        if self.mcclient.get(self.tagLastUpdateOn) == None:
            self.mcclient.set(self.tagLastUpdateOn, time.time()) == None
        if self.mcclient.get(self.tagHeartBeat) == None:
            self.mcclient.set(self.tagHeartBeat, time.time())
            
        if self.mcclient.get(self.tagLastState) == None:
            self.mcclient.set(self.tagLastState, current_state)
        if self.mcclient.get(self.tagCurrentState) == None:
            self.mcclient.set(self.tagCurrentState, time.time())
            
    def getStats(self):
        
        print self.mcclient.get_stats()
        
    def setState(self, state, lastupdateon):
        
        self.mcclient.set(self.tagLastState, state)
        self.mcclient.set(self.tagLastUpdateOn, lastupdateon)
    
    def getState(self):
        
        s = self.mcclient.get(self.tagLastState)
        u = self.mcclient.get(self.tagLastUpdateOn)
        return (s,u)
    
    def beat(self):
        
        #print self.tagHeartBeat
        #log.debug( self.mcclient.get_stats() )
        now = time.time()
        self.mcclient.set(self.tagHeartBeat, now)
        #log.debug("set beat time")
        
    def getHeartBeat(self):
        return self.mcclient.get(self.tagHeartBeat)
        
    def checkHeartBeat(self):
        
        lastheartbeat =  self.mcclient.get(self.tagHeartBeat)
        if lastheartbeat == None:
            #self.beat()
            self.tagInit()
            raise Exception('No Heart Beat')
        #print strftime('%Y-%m-%d %H:%M:%S',localtime(timestamp))
        #return ''
        now = time.time()
        
        TDelta = now - lastheartbeat
        current = strftime('%Y-%m-%d %H:%M:%S', localtime())
        print "[%s]%s beat check: %s / %s"%(current, self.device, TDelta, self.HBThreshold)
        if TDelta> self.HBThreshold:
            #raise Exception('No Heart Beat!')
            print "[%s]%s beat check: %s / %s"%(current, self.device, TDelta, self.HBThreshold)
            self.report()
        else:
            #print TDelta
            pass
    
    def report(self):
        
        #self.mcclient.delete(self.tagLastReportOn)
        lastReportOn =  self.mcclient.get(self.tagLastReportOn)
        now = time.time()
        #print lastReportOn
        if lastReportOn == None:
            
            self.sendMail()
            self.mcclient.set(self.tagLastReportOn, now) 
        
        elif now - lastReportOn > self.ReportInterval:
            
            self.sendMail()
            self.mcclient.set(self.tagLastReportOn, now)        
            
            
        else:
            print now - lastReportOn
            pass
        
    def sendMail(self):
        log.debug( "Send Email" )
        mailclient = Sendmail()
        #mfrom, mto, subject, html_part
        html_part = u"""<html><header/>
        <body>
          <h1>你好!</h1>
          <a href="http://fcecspmests02.ced.corp.cummins.com/testinfo/cells/1">Real Time State</a>
          Please Check <b>%s</b>.
        </body>
        </html>   
        """%(self.device )
        
        #mailclient.send('jianjun.ma@cummins.com','jankin.ma@mabotech.com', 'please check AVL Monitor', html_part)
        
        pass
    

def doit(state):
    

        #state.beat()
    try:
        state.checkHeartBeat()
    except Exception, e:
        print e
        pass
    
    #print "--"*20
    dur = 10
    reactor.callLater(dur, doit, state)
    
    
    
def main():


    wsdict = {
          'TestZone2_TC1':'TestZone2_TC1',
          'TestZone6_TC2':'TestZone6_TC2',
          'TestZone2_TC3':'TestZone2_TC3',
          'TestZone6_TC4':'TestZone6_TC4',
          'TestZone2_TC5':'TestZone2_TC5',
          'TestZone6_TC6':'TestZone6_TC6',
          'TestZone2_TC7':'TestZone2_TC7',
          'TestZone6_TC8':'TestZone6_TC8',
          'TestZone2_TC9':'TestZone2_TC9',
          'TestZone6_TC10':'TestZone6_TC10',
          'TestZone2_TC11':'TestZone2_TC11',
          'TestZone6_TC12':'TestZone6_TC12',
          'TestZone2_TC13':'TestZone2_TC13' ,
          'TestZone6_TC14':'TestZone6_TC14',  
          }
          
    for device in wsdict:
    
        state = StateCache(device)
        #device = 'TestZone6_TC12'
        dur = 3
        #state = StateCache(device)
        #state.beat()
        reactor.callLater(dur, doit, state)
    reactor.run()    
    
    
  
  
if __name__=='__main__':
  
  main()
  
  
  
  
  
  
  
  
  
  
  
"""  
#from timeit import Timer
#t = Timer("main()", "from __main__ import main")
#print t.timeit(number=1)
"""



