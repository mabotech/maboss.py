# -*- coding: utf-8 -*-


import os

import ConfigParser

#from common.singleton import Singleton

class Config(object):

  # Singleton Class
  #__metaclass__ = Singleton

  def __init__(self,file):
    
    self.conf = ConfigParser.RawConfigParser()
    
    filename = '%s' %(file)
    
    if os.path.exists(filename):

        self.cfgpath = filename
    
    else:
        
        path = os.getcwd() #path+"\\"+
        #path = os.path.abspath("..")
        p = ".."
        i = 0
        while not os.path.exists(path + "\\"+filename):
          path = os.path.abspath(p)
          p = p+"\\.."
          i = i +1
          if i >4:
            break
          #print path
        self.cfgpath = path+"\\"+filename
    try:
      
      #print self.cfgpath
      self.f = open(self.cfgpath,"r")
      self.conf.readfp(self.f)
    except Exception, e:
        
      #print e
      info = "fail to open: %s " %( path+"\\"+filename )
      raise Exception(info)


  def sections(self):
      return self.conf.sections()
      
  def getOption(self, section, option):
    if self.conf.has_option( section,option):
      #print self.conf.get(section,option)
      return self.conf.get(section,option)
    else:
      raise Exception( "could not find "+ option )

  def setOption(self,section, option,value):
      """
        if self.conf.has_option( section,option):
          return 0
        else:
      """
      self.conf.set( section, option, value)
      newc = open(self.cfgpath,"w")
      #print newc
      self.conf.write(newc)
      #print "write to conf"

  def options(self,section):
    return self.conf.options(section)

  def removeOption():
    pass

class ConfigObj(object):

    def __init__(self):
        pass


