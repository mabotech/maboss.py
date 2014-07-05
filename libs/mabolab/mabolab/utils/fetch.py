# -*- coding: utf-8 -*-

import os
import glob

import operator

from subprocess import Popen, PIPE

from time import time, strftime, localtime


class RRD:
  
  def __init__(self):
    
    self.data = {}
    
    self.sortedData = {}
    
    self.max = {}
    
    list = ['cpu_util','disk_bytes_transferred','mem_available_bytes','net_bits_out']
    
    cpu_util = {}
    disk_bytes_transferred = {}
    mem_available_bytes = {}
    net_bits_out = {}
    
    
  def getInfo(self, r):
    files = glob.glob("C:\\opt\\KServer\\kserver\\public\\*.rrd")
    i = 1
  
  
    for f in files:
      #if f in ['FCECSPMESPU01.ced.corp.cummins.com','FCECSPMESADM01.ced.corp.cummins.com']:
      #  continue
      i = i + 1
      #if i > 8:
      #  break
      if r == 28800:
        cmd = "C:\\opt\\KServer\\kserver\\public\\lib\\rrdtool fetch %s AVERAGE  -r 28800 -s -1day "%(f) #86400
      else:
        cmd = "C:\\opt\\KServer\\kserver\\public\\lib\\rrdtool fetch %s AVERAGE  -r 60 -s -2min "%(f) #86400
      #print cmd
      filename = os.path.basename(f)
      left = filename.find('_')
      #print "%s - %s"%(filename[:left], filename[left+1:].split('.')[0])
      host = filename[:left]
      mtype = filename[left+1:].split('.')[0]
      #print "%s - %s"%(host,mtype)
      p = Popen(cmd, shell=True, stdout=PIPE)
      info = p.stdout.read()
      x = info.split('\n')
      
      
      
      #for n in range(2,3):
        #print n
      v = x[2].strip()
      l = v.split(': ')
      try:
        #print strftime('%Y-%m-%d %H:%M:%s',localtime(int(l[0])))    
        #print float(l[1])
        value = float(l[1])
      except:
        #print "-1.#IND000000e+000"
        value = 0
        pass
      #print value
      
      if value > 100000000000 and mtype == 'net_bits_out':
        #print host, mtype, value
        value = value / 100000000.0
      
      if self.data.has_key(mtype):
        pass
      else:
        self.data[mtype] = {}
        
      if self.max.has_key(mtype):
        pass
      else:
        self.max[mtype] = 0
        
      if self.max[mtype] < value:
        self.max[mtype] = value
        
      self.data[mtype][host] = value
      
      
      
      #print "="*20
      
  def getData(self):
    return self.data
    
  def getSortedData(self):
    for item in self.data:
      kv = self.data[item]
      sortedData =sorted(kv.iteritems(), key=operator.itemgetter(1), reverse=True)
      self.sortedData[item] = sortedData
      
    return self.sortedData
      
    
  def getMax(self):
    return self.max    
  
  
if __name__ == '__main__':
    list = ['cpu_util','disk_bytes_transferred','mem_available_bytes','net_bits_out']
    rrd = RRD()
    rrd.getInfo(28800)
    print rrd.getMax()
    info = rrd.getData()
    st = rrd.getSortedData()
    print st
    for item in list:
      print info[item]
      sortedData =sorted(info[item].iteritems(), key=operator.itemgetter(1), reverse=True)
      print sortedData
      for host in info[item]:
        print host, info[item][host]
      print "=="*20
