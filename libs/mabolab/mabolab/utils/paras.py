# -*- coding: UTF-8 -*-
# post xml soap message

import sys, httplib
from twisted.internet import threads, reactor
from sqlalchemy import *
from time import localtime, strftime
import pyRXP

import logging.handlers, logging.config

#logging.config.fileConfig('log.ini')
#log= logging.getLogger('OPCConnect')
import urllib
import urllib2

from singleton import Singleton

class SOAPParser:

    __metaclass__ = Singleton

    def __init__(self):
      self.paras = {}
      self.deep = 0
      pass
      
    def xml2doctree(self, xml):
        pyRXP_parse = pyRXP.Parser(
            ErrorOnValidityErrors=1,
            NoNoDTDWarning=1,
            ExpandCharacterEntities=0,
            ExpandGeneralEntities=0)
        return pyRXP_parse.parse(xml)


    def getParsed(self):
        return self.parsed

    def parse(self, xml):
        #print xml
        self.paras = {}
        self.deep = 0
        self.parsed = self.xml2doctree(xml)

        return self.parsed

    def getNode(self, node):
        #print node
        self.deep = self.deep + 1
        for item in node:
            if isinstance(item, list) or isinstance(item, tuple):
                #print item[0]
                if item[0] == 'EmployeeID':
                  self.paras['EmployeeID'] = item[2][0]
                elif item[0] == 'OperationID':
                  #('LiteralID', None, ['FlexNet.SystemServices.StandardOutcomeResult.Failure'], None)
                  #('LiteralID', None, ['FlexNet.SystemServices.StandardOutcomeResult.Success'], None)
                  #print item[2][0]
                  self.paras['OperationID'] = item[2][0]
                elif item[0] == 'PropertyBagItem':
                  #print item[1]['Key'],item[2]#[2][0][2][0]
                  if item[2][0][2] == None:
                    self.paras[item[1]['Key']] = None
                  else:
                    self.paras[item[1]['Key']] = item[2][0][2][0]

                else:
                    if self.deep < 8:
                      self.getNode(item)
            else:
                #print item
                pass


def getParas(xml):
  sp = SOAPParser()
  root = sp.parse(xml)
  sp.getNode(root)
  #print sp.paras
  return sp.paras
  
if __name__ == "__main__":
  
  xml = '''<?xml version="1.0" encoding="utf-8"?><OperationInterpretationParameters xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><OperationID>100000862</OperationID><OperationResolutionMethod>ByOperationID</OperationResolutionMethod><Inputs><PropertyBagItem Key="WorkOrder"><Value xsi:type="xsd:string">SO10103000003</Value></PropertyBagItem><PropertyBagItem Key="TriggeringStation"><Value xsi:type="xsd:string">36400</Value></PropertyBagItem><PropertyBagItem Key="Event"><Value xsi:type="xsd:string">Broadcast</Value></PropertyBagItem></Inputs><SystemVariables><PropertyBagItem Key="OPRSEQUENCENO"><Value xsi:type="xsd:string" /></PropertyBagItem><PropertyBagItem Key="CURRENTTASKID"><Value xsi:type="xsd:int">-1</Value></PropertyBagItem><PropertyBagItem Key="WIPORDERTYPE"><Value xsi:type="xsd:int">-1</Value></PropertyBagItem><PropertyBagItem Key="REASONCODE"><Value xsi:type="xsd:string" /></PropertyBagItem><PropertyBagItem Key="WIPORDERNO"><Value xsi:type="xsd:string" /></PropertyBagItem><PropertyBagItem Key="EMPLOYEEID"><Value xsi:type="xsd:int">63</Value></PropertyBagItem><PropertyBagItem Key="LANGUAGEID"><Value xsi:type="xsd:int">1033</Value></PropertyBagItem><PropertyBagItem Key="WORKCENTER"><Value xsi:type="xsd:string" /></PropertyBagItem><PropertyBagItem Key="EQUIPMENTID"><Value xsi:type="xsd:int">0</Value></PropertyBagItem><PropertyBagItem Key="ALERTID"><Value xsi:type="ArrayOfInt" /></PropertyBagItem><PropertyBagItem Key="TASKID"><Value xsi:type="xsd:int">-1</Value></PropertyBagItem></SystemVariables><SerializedContextProperties>%00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%1b__EmployeeAttendanceTracked%08%01%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0e__FunctionName%06%04%00%00%00%05SubOp%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00!__EmployeeAutoCloseLaborOnClockIn%08%01%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%11OperationRevision%06%04%00%00%00%072.8.038%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0bOperationID%08%08%f6%e9%f5%05%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0c__EmployeeNo%06%04%00%00%00%06System%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0a__Facility%06%04%00%00%00%05BFCEC%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00!__EmployeeAutoClockInOnStartLabor%08%01%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0dOperationCode%06%04%00%00%00%13COB_SO_WS_OPERATION%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0c__TimeZoneID%08%08_%04%00%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0b__DbCulture%08%08%09%04%00%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%12__CustomProperties%09%04%00%00%00%05%04%00%00%00%22FlexNet.SystemServices.PropertyBag%01%00%00%00%13CollectionBase%2blist%03%1cSystem.Collections.ArrayList%02%00%00%00%09%05%00%00%00%04%05%00%00%00%1cSystem.Collections.ArrayList%03%00%00%00%06_items%05_size%08_version%05%00%00%08%08%09%06%00%00%00%00%00%00%00%06%00%00%00%10%06%00%00%00%10%00%00%00%0d%10%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%16__EmployeeLaborTracked%08%01%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%0c__EmployeeID%08%08%3f%00%00%00%0b %00%01%00%00%00%ff%ff%ff%ff%01%00%00%00%00%00%00%00%0c%02%00%00%00YFlexNet.SystemServices%2c+Version%3d9.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d33f692327842122b%05%01%00%00%00%26FlexNet.SystemServices.PropertyBagItem%02%00%00%00%04_Key%06_Value%01%02%02%00%00%00%06%03%00%00%00%10__StepSequenceNo%08%08%0a%00%00%00%0b </SerializedContextProperties><EmployeeID>63</EmployeeID></OperationInterpretationParameters>'''
  
  p = getParas(xml)
  
  print p



