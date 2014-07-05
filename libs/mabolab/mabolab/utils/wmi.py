

import threading

import win32com.client

#from singleton import Singleton

import threading
import pythoncom

import time

import logging

#log = __import__('logging').getLogger(__name__)

log = logging.getLogger(__name__)


class WMI:

    #__metaclass__ = Singleton

    def __init__(self, computer, namespace, username, password):


        #self.WQL = WQL
        
        log.info('WMI init...[%s]' %(computer))
        
        self.threadName = threading.currentThread ().getName ()

        #log.debug('-----------thread name---------------')
        #log.debug(threading.currentThread ().getName ())

        if self.threadName  <> 'worker 0':  # 'MainThread'
            pythoncom.CoInitialize ()

        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")

        if computer == ".":
            self.objSWbemServices = objWMIService.ConnectServer(computer,namespace)

        else:
            self.objSWbemServices = objWMIService.ConnectServer(computer,namespace, username,password)

        self.keys = []
        self.values = []
        self.kv = {}
        
    def getThreadName(self):
        return self.threadName

    def queryState(self, service):
        
        wql = """Select name, state  from Win32_Service where name = "%s" """ %(service)
        colItems = self.objSWbemServices.ExecQuery(wql)
        
        if len(colItems)>0:
            return colItems[0].state
        else:
            return None
        
    def stopService(self, service):
        
        wql = """Select * from Win32_Service where name = "%s" """ %(service)
        
        colItems = self.objSWbemServices.ExecQuery(wql)
        
        for objItem in colItems:

            #print objItem.Caption,
            #print objItem.Description,
            
            info = "%s:%s"%(objItem.Name,  objItem.Status)
            #print info
            #log.debug(info)
            
            objItem.StopService        
            
    def restartService(self, service):       
        
        wql = """Select * from Win32_Service where name = "%s" """ %(service) #FlexNetJobExecutorService
        
        colItems = self.objSWbemServices.ExecQuery(wql)   

        if len(colItems)>0:
            
            colItems[0].StopService
            i = 0
            while 1:
                i = i + 1
                if i > 20:
                    break
                state =  self.queryState(service)
                if state == 'Stopped':
                    break
                time.sleep(0.5)
            
            colItems[0].StartService
        else:
            
            log.debug("can't find this service[%s]" % (service))
            
            pass
            #raise Exception("can't find this service[%s]" % (service) )
            
    def restartService2(self, service):
        
        wql = """Select * from Win32_Service where name = "%s" """ %(service) #FlexNetJobExecutorService
        
        colItems = self.objSWbemServices.ExecQuery(wql)
        
        for objItem in colItems:

            #print objItem.Caption,
            #print objItem.Description,
            
            info = "%s:%s"%(objItem.Name,  objItem.Status)
            #print info
            #log.debug(info)
            
            objItem.StopService
            
            #time.sleep(30)
            
            objItem.StartService        


    def startService(self, service):
        
        wql = """Select * from Win32_Service where name = "%s" """ %(service) #FlexNetJobExecutorService
        
        colItems = self.objSWbemServices.ExecQuery(wql)
        
        for objItem in colItems:

            #print objItem.Caption,
            #print objItem.Description,
            
            info = "%s:%s"%(objItem.Name,  objItem.Status)
            #print info
            #log.debug(info)
            
            #objItem.StopService
            
            time.sleep(0.5)
            
            objItem.StartService 

    def query(self, wql):

        self.keys = []
        self.values = []

        #print "wql:%s"%(wql)
        colItems = self.objSWbemServices.ExecQuery(wql)

        i = 0

        #print type(colItems)

        for objItem in colItems:
            valarr = []

            for item in objItem.properties_:
                valarr.append(item.value)
                if i == 0:
                    #print item.name
                    self.keys.append(item.name)

            self.values.append(valarr)
            #self.kv[item.name] = item.value

            valarr = []

            i = i + 1
        #print (self.keys, self.values)
        return (self.keys, self.values)

    def getKeys(self, result= None):
        #print self.keys
        return self.keys

    def getValues(self, result=None):
        #print self.values
        return self.values

    def printInfo(self):

        #print self.keys

        for val in self.values:
            #print val
            pass

        """
        print item.name,
        if isinstance(item.value, unicode):
            print item.value.encode('utf8')
        else:
            print item.value
        #item.value.encode('utf8')
        """

    def __del__(self):

        #print "deleted"
        pass
