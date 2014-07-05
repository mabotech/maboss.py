# -*- coding: utf-8 -*-


#register_printer

import os

import win32netcon
import win32wnet
import win32api
from win32wnet import NETRESOURCE  

import logging
import logging.config 


import time

from utils import open_cmd, get_token

import static

from configuration import PrinterConfiguration



logger = logging.getLogger(__name__)


class PrinterConnection(object):
    
    def __init__(self, config):
        
        self.config = config
        
        
    def add_connection(self, local, remote, username, passwd):

        logger.debug("net use %s %s /user:%s" % (local, remote, username) )
        
        logger.debug("user: "+win32api.GetUserName() )
        
        
        if static.DEBUG == True:   
            
            type = win32netcon.RESOURCETYPE_DISK
            
        else:
            type = win32netcon.RESOURCETYPE_PRINT  
        
        nr = NETRESOURCE()  
        
        nr.dwScope = win32netcon.RESOURCE_CONNECTED  
        nr.dwType = type
        nr.lpLocalName = local
        nr.lpProvider = ''  
        nr.lpRemoteName = remote
        nr.dwUsage = win32netcon.RESOURCEUSAGE_CONNECTABLE      
      
        
        try:
            
            #logger.debug("type:%s" % (type) )
            
            #win32wnet.WNetAddConnection2(nr, passwd, username)
            cmd = "net use %s /user:Administrator B0st0nP" % (remote)
            #cmd = "net use %s" % (remote)
            logger.debug(cmd)
            open_cmd(cmd)
            #logger.debug(rtn)
            #time.sleep(1)
            #logger.debug( str(win32wnet.WNetGetResourceInformation(nr) ) )

            logger.debug( win32wnet.WNetGetConnection(local)  )
            
        except Exception, e:
            
            logger.debug( e  )
        
    def cancel_connection(self, local, remote):
        
        logger.debug("net use /delete %s" %(local) )
        
        try:
            
            #win32wnet.WNetCancelConnection2(local, 1, 1)
            cmd = "net use  /del %s " % (remote)
            open_cmd(cmd)
            
        except Exception, e:
            
            logger.debug( e  )        

    def connect(self):
        
        logger.debug("register printer")
        
        """
        net use lpt1 \\192.168.40.49\ZebraTLP2844 /user:Administrator B0st0nP
        """
        
        #print self.config
        
        address_list = self.config['address_list']
        
        lpt_list = self.config['lpt_list']
        
        
            
        #print address_list
        
        for x in address_list:
            address =  address_list[x]
            
            lpt =  lpt_list[x]
            

            #cmd = r"net use %s %s /user:Administrator B0st0nP" %(lpt,  address )
            
            self.cancel_connection(lpt, address)
            
            self.add_connection(lpt, address, "Administrator", "B0st0nP")
            
            
            """
            cmd = r"net use /delete %s" %(lpt )
            
            open_cmd(cmd)
            
            token = get_token(static.LOGIN_TOKEN)
            
            cmd = r"net use %s %s /user:%s" %(lpt,  address, token)
            
            open_cmd(cmd)
            """

                
                
if __name__ == "__main__":
        
        pc = PrinterConfiguration()
        
        pc.download_config()
        
        config = pc.get_config()
    
        
        reg =  PrinterConnection(config)
        
        reg.run()
        
