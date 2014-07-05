# -*- coding: utf-8 -*-

import httplib

import simplejson

import logging
import logging.config 

#logging.config.fileConfig('C:/BPMES/print_manager/logging.ini')

logger = logging.getLogger(__name__)


import static

class PrinterConfiguration(object):
    
    def __init__(self):
        
        self.data = ""
        
        self.config = {}
        
        self.printer_address = {}
        
        self.printer_lpt = {}
        
        self.lpt_address = {}
        
        self.printer_pwd = {}        
        
    
    def save_json(self):
        
        fh = open("printers.json","w")
        
        fh.write(self.data)
        
        fh.close()
        
        
        
    def get_config(self):
        
        self.config['address_list'] = self.printer_address
        self.config['lpt_list'] = self.printer_lpt
        self.config['lpt_map'] = self.lpt_address
        
        logger.debug(self.config)
        
        return self.config
        
        
    
    def download_config(self):

    
        try:
            
            conn = httplib.HTTPConnection(static.CONFIG_SERVER)
            
            url = "/Mabo/utils/Service.aspx?opcode=MT_SO_GetConfig" 
            
            i_url = "http://"+static.CONFIG_SERVER + url
            
            logger.debug(i_url)
            
            conn.request("GET", url)            

            #conn.request("GET", "/")

            resp = conn.getresponse()

            self.data = resp.read()
            
            logger.debug( self.data )
            
        except Exception, e:
            
            logger.debug("download configuration failed") 
            logger.debug(e)
            
            #logger.debug ( "%s,%s" %( resp.status, resp.reason ))
            
            self.get_local_config()
            
            raise(Exception(e.message))
            
            #raise(Exception("can't download config json"))
     
    def get_local_config(self):
        
            fh = open("printers.json","r")
            
            self.data = fh.read()             

            logger.debug(self.data)

            fh.close()    
            
    def set_config(self):
        
            
            if static.LOCAL_CONFIG != True:
                
                self.download_config()
        
                self.save_json()                
            
            else:
                logger.debug("load backup config")     
                self.get_local_config()
            
            #v= self.data.replace('\\','\\\\')            

            x = simplejson.loads(self.data)

            i = 0
            j = -1
            for a in  x['spooladdress']:
                
                
                if a [0:2] != "\\\\":
                    i = i +1
                    logger.debug(a)
                    continue
                else:
                    j = j +1
                    
                
            
                key = x['printerid'][i]
                
                self.printer_address[key] = a
                
                #i = i + 1
                if static.DEBUG == True:
                    v = "%s:" % (chr(78+i))
                else:
                    v = "LPT%s" % (j) #int(key) - 100000000)
                self.printer_lpt[key] = v
                self.lpt_address [v ] = a
                i = i + 1
            



    def show(self):
        
        """
        print self.printer_address
        
        print self.printer_lpt
        
        print self.lpt_address
        """


if __name__ == '__main__':
    
    
    
    pc = PrinterConfig()
    
    pc.set_config()
    
    v = pc.get_config()
    
    print v
    
    
