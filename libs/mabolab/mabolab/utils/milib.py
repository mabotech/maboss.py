
import time
import threading
import win32com.client
import pythoncom

import logging
log = logging.getLogger(__name__)

class ServicesManager:
    
    def __init__(self):
        
        if threading.currentThread ().getName () <> 'worker 0':
            pythoncom.CoInitialize ()
        
        self.objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        
        

    def restartServices(self, host, username, password):        
        
        self.objSWbemServices = self.objWMIService.ConnectServer(host,"root\cimv2",username, password)
        
        #objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        
        wql = """Select * from Win32_Service where name = "FlexNetMachineConnector" """
        
        colItems = self.objSWbemServices.ExecQuery(wql)
        
        for objItem in colItems:

            #print objItem.Caption,
            #print objItem.Description,
            
            info = "%s:%s"%(objItem.Name,  objItem.Status)
            #print info
            log.debug(info)
            
            objItem.StopService
            
            time.sleep(0.5)
            
            objItem.StartService



if __name__ == "__main__":
    
    host ="fcecspmesapp01.ced.corp.cummins.com"

    username = 'ced\\fcecmesmq'#""  #'ced\\fcecmesmq',"Fcec!@#$72"

    password = "Fcec!@#$72"#"P@ssw0rd"
    
    #host = 'fcecmes01c36455'
    #username = 'Administrator'
    #password = "P@ssw0rd"
    
    sm = ServicesManager()
    
    sm.restartServices(host, username, password)
