# -*- coding: utf-8 -*-

import random
import unittest

class TestWMIFunctions(unittest.TestCase):

    def setUp(self):
        
        from mabo.utils.wmi import WMI
        
        

        #print wql2
        
        host = "." #"10.10.128.132"
        username = "sgmytprd\\administrator"
        password = "ytpassword"
        self.wmiobj = WMI(host, "root\cimv2", username, password)

    def test_getThreadName(self):
        
        print self.wmiobj.getThreadName()
        

    def test_item(self):
        wql = '''select name, state from win32_service where name like "FlexNet%" or name ="W3SVC" or name = "aspnet_state" '''
        rtn =self.wmiobj.query(wql)[0]        
        self.assertEqual(rtn, [u'Name', u'State'])
         
    def test_all(self):
        self.wmiobj.getKeys()
        self.wmiobj.getValues()        


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
    
"""
    srvs = ['FlexNetProcessBuilderServices', 'FlexNetProcessDataConnectorServices','FlexNetSchedulingService']

    clause = ""
    for item in srvs:
        clause =  '%s or name = "%s"' %(clause, item)

    wql2 = '''select caption, name, status, state from win32_service where name='1' %s'''%(clause)
    wql2 = '''select name, state from win32_service where name='1' %s'''%(clause)

    #wql2 = '''select caption, name, status, state from win32_service where name='1' or name = "FlexNetProcessBuilderServices" or name = "FlexNetProcessDataConnectorServices" or name = "FlexNetSchedulingService"'''
    wql = '''select caption, name, status, state from win32_service where name like "FlexNet%"'''

    wql = '''select name, state from win32_service where name like "FlexNet%" or name ="W3SVC" or name = "aspnet_state"'''

    #print wql2
    
    host = "." #"10.10.128.132"
    username = "sgmytprd\\administrator"
    password = "ytpassword"
    wmiobj = WMI(host, "root\cimv2", username, password,wql)
    wmiobj.query()
    wmiobj.getKeys()
    wmiobj.getValues()

    wmiobj.printInfo()
    #wmiobj.restartJE()
    wmiobj.stopJE()
"""    