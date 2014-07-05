# -*- coding: utf-8 -*-

import httplib

import simplejson

import logging
import logging.config 

log = logging.getLogger(__name__)

class JSONConfiguration(object):
    
    def __init__(self):
        
        self.data = ""     
    
    
    def save_json(self):
        
        fh = open("printers.json","w")        
        fh.write(self.data)        
        fh.close()        
        
        
    def get_config(self):
        
        self.download_config()
        #print self.data
        x = simplejson.loads(self.data)
        #print x['printers']
        inner_cfg = {}
        for item in x['printers']:
            #print item
            inner_cfg[item['station']] = item
        #print inner_cfg
        
        if '36000' in inner_cfg:
            print inner_cfg['36000']['IP']
        
    def download_config(self):

        host = '127.0.0.1'
        port = 8080
        
        url = "/configuration/printers.json" 
        
        log.debug("download configuration:%s:%s%s" % (host, port, url) )
        
        try:
            
            conn = httplib.HTTPConnection(host, port)
            
            
            
            #i_url = "http://"+static.CONFIG_SERVER + url
            
            log.debug(url)
            
            conn.request("GET", url)            

            #conn.request("GET", "/")

            resp = conn.getresponse()

            self.data = resp.read()
            
            log.debug( self.data )
            
        except Exception, e:
            
            log.debug("download configuration failed") 
            log.debug(e)
            
            #logger.debug ( "%s,%s" %( resp.status, resp.reason ))
            
            #self.get_local_config()
            
            raise(Exception(e.message))
            
            #raise(Exception("can't download config json"))
     
    def get_local_config(self):
        
            fh = open("printers.json","r")
            
            self.data = fh.read()             

            logger.debug(self.data)

            fh.close()    
            



if __name__ == '__main__':
    
    
    
    pc = JSONConfiguration()
    
    #pc.set_config()
    
    v = pc.get_config()
    
    print v
    
    
