
import sys
import re
import os
import shutil

from time import time, localtime, strftime

import csv

class  ControlWord:

  def __init__(self):
    MES = """00 not define
01 not define
02 not configured for this production line
03 Engine is being reflowed
04 MES is configured for AMI download
05 Load From Repair
06 Send To Repair
07 MES complete
08 Sequential part Failsafing
09 MES Data Received
10 Failsafes Sent
11 Torque Failsafing
12 Orientation Failsafing
13 Part Selection Failsafing
14 Engine Stop Build
15 Engine Build to Kit"""

    PLC = """00 Engine arrival
01 Engine depart
02 Engine complete
03 Station Override
04 Engine failsafe received
05 Engine failsafe complete
06 Data Ready
07 Part Selection Failsafe Fail
08 Torque Failsafe Fail
09 Torque Data Fail
10 Orientation Failsafe Fail
11 Station Fault
12 Station Reset
13
14
15"""

    self.mesl = MES.split('\n')
    self.plcl = PLC.split('\n')

    # http://en.literateprograms.org/Binary_numeral_conversion_(Python)
  def bin(self, n):
      if n < 0:
          return "-" + alt_bin(-n)
      s = ''
      while n != 0:
          if n % 2 == 0: bit = '0'
          else: bit = '1'
          s = bit + s
          n >>= 1
      return s or '0'

  #print int("10000000000", base=2)

  #print mesl

  def mes(self, x):
    rt = ""
    bit = self.bin(x) #"1001"
    rt = rt +  "[%016d]"%(int(bit))
    #print "%s, %s" %(x, bit)
    if bit == '0':
      rt = rt +   "reset\n"
    else:
      lb = len(bit)
      for x in range(0, lb):
        if bit[x] == '1':
          b = (lb -1) - x
          rt = rt +   "%s --- " %(self.mesl[b])
      rt = rt +  '\n'
    return rt

  def plc(self, x):
    rt = ""
    bit = self.bin(x) #"1001"
    rt = rt +   "[%016d]"%(int(bit))
    #print "%s, %s" %(x, bit)
    if bit == '0':
      rt = rt +   "reset\n"
    else:
      lb = len(bit)
      for x in range(0, lb):
        if bit[x] == '1':
          b = (lb -1) - x
          rt = rt +   "%s --- " %(self.plcl[b])
      rt = rt +  '\n'
    return rt




class MILogAnalyzer:

    def __init__(self, mihost, workstation):
        self.mihost = mihost
        self.workstation = workstation
        self.dst = "D:\\workspace\\projects\\MI_%s_DebugRolling.log" %(mihost)
        self.loglines = []

    def fetchall(self):
        self.main()
        rtn = []
        lines = self.linesReverse()
        for line in lines:
            l = []
            l.append(line)
            rtn.append(l)

        return rtn

    def linesReverse(self):

        self.loglines.reverse()

        return self.loglines

    def color(self):

      fn = 'mi_%s.html'%(self.mihost)
      output = file(fn,'w')
      head = """
      <html>
      <head><title>%s</title>
      <style type="text/css">
      </style>
      </head>

      <body>
      <table border="1" cellpadding="0" cellspacing="0">
      """ %(self.mihost)
      output.write(head)
      #if len(input)>0:
      #  input = input.reverse()
      #print dir(input)

      #print type(input)

      for line in self.loglines:

        line = line.replace('>', "&gt;")
        line = line.replace('<', "&lt;")

        line = line.replace('Station Reset','<font color="red">Station Reset</font>')

        line = line.replace('[MES],', "[MES]<br>")
        line = line.replace('[PLC],', "[PLC]<br>")
        if line.count('[MES]')>0:
          oneline = """
      <tr bgcolor="#FFFFCC"><td><font color="#CC3333">%s</font></td></tr>
          """ %(line)
        elif line.count('ESNNumber')>0:
          oneline = """
      <tr><td><font color="blue">%s</font></td></tr>
          """ %(line)
        else:
          oneline = """
      <tr><td>%s</td></tr>
          """ %(line)
        output.write(oneline)


      tail = """
      </table>
      </body>
      </html>
      """

      output.write(tail)
      output.close()
      cmd = '"e:\\Program Files\\Mozilla Firefox\\firefox.exe" %s' %(fn)
      #print cmd
      #os.system(cmd)
      rt = os.popen(cmd)
      print (rt.read())


    def downloadLog():

      #
      if string.find(self.mihost,'mes')<0:
        cmd = r"""net use \\fcecmes01c%s\c$ /user:fcecmes01c%s\Administrator P@ssw0rd""" %(self.mihost,self.mihost)
        fn = r'\\fcecmes01c%s\c$\Temp\FlexNetLogs\MachineIntegratorService_DebugRolling.log' %(self.mihost)

      else:
        cmd = r"""net use \\%s\c$ /user:ced\fcecmesmq Fcec!@#$72""" %(self.mihost)
        fn = r'\\%s\c$\Temp\FlexNetLogs\MachineIntegratorService_DebugRolling.log' %(self.mihost)


      print cmd
      rt = os.popen(cmd)
      print (rt.read()),
      #print x



      #fn = 'log1.txt'

      try:
        print fn,self.dst
        if os.path.exists(dst):
          f01 =  os.stat(fn)
          f02 =  os.stat(self.dst)
          #compare files createdon
          if f01[6] != f02[6]:
            shutil.copyfile(fn,self.dst)
        else:
          print fn,self.dst
          shutil.copyfile(fn,self.dst)

        pass
      except Exception, e:
        print e



    def main(self):

      input = file(self.dst, 'r')
      cw = ControlWord()
      i = 0
      rawstr = r"""(.*)for point '.*\\Softnet\\(.*)\\(.*)ControlWord'"""
      rawstr2 = r"""Received change notification for point: .*Softnet\\(.*)ControlWord, new value: (.*),.*""" #new value: 55,

      compile_ctrl = re.compile(rawstr,  re.IGNORECASE)

      compile_obj2 = re.compile(rawstr2,  re.IGNORECASE)

      rawstr3 = r""" (.*) value \((.*)\)"""
      compile_obj3 = re.compile(rawstr3,  re.IGNORECASE)

      lines =[]

      #raw1 = r"""(.*)FlexNet.MachineIntegrator.SystemServices.CoreEngine.MachineIntegrator"""
      raw1 = r"""(.*?),(\d+) DEBUG (\d+) FlexNet.MachineIntegrator.SystemServices.CoreEngine.MachineIntegrator"""
      compile_obj4 = re.compile(raw1,  re.IGNORECASE)

      rstr = r"""Value: (.*) Quality:.*UOM: """
      compile_obj5 = re.compile(rstr,  re.IGNORECASE)

      setval = r"""et value (\d+) for point"""
      compile_setval = re.compile(setval,  re.IGNORECASE)

      for line in input:

        lines.append(line)

      ln = 0
      out = ""
      linetype = 0
      for line in lines:
        if self.workstation != None:
          if line.count(self.workstation)>0:
            pass
          else:
            continue
        linetype = 0
        if line.count('ESN') > 0:
          logon = compile_obj4.search(lines[ln-1])
          if logon:
            out = out + logon.group(1)
          out = out + line
        #print line,

        #ControlWord
        match_ctrl = compile_ctrl.search(line)

        #received
        match_obj2 = compile_obj2.search(line)



        if match_ctrl:
          linetype = 1
          group_1 = match_ctrl.group(1)
          group_2 = match_ctrl.group(2)
          group_3 = match_ctrl.group(3)

          #set/get value
          match_obj3 = compile_obj3.search(group_1)
          if match_obj3:
            group_31 = match_obj3.group(1)

            group_32 = match_obj3.group(2)
            #print lines[ln-1],

            if group_31.startswith('Set'):
              out = out +  '<--'
            else:
              out = out + '-->'
              #Value: 1 Quality
          logon = compile_obj4.search(lines[ln-1])

          gv = compile_obj5.search(group_32)

          if gv:
            xx = gv.group(1)
            try:
              out  = out +  "%s, [%s],%s,[%s],%sControlWord" %(logon.group(1), gv.group(1),group_2,group_3, group_3)
            except:
              pass
          else:
            xx = group_32
            if logon:
              out = out +  "%s, [%s],%s,[%s],%sControlWord" %(logon.group(1), group_32,group_2,group_3, group_3)
            else:
              out = out +  "[%s],%s,[%s],%sControlWord" %(group_32,group_2,group_3, group_3)

          if group_3.upper() == 'MES':
            #print 'mes'
            if xx == 'Null':
              continue
            else:
              rt = cw.mes(int(xx))
              out = out +  rt
          elif group_3.upper() == 'PLC':
            #print 'plc'
            try:
              rt = cw.plc(int(xx))
              out = out +  rt
            except:
              print ("PLC value: %s", xx)
          #print ("%s-%s" %(group_1, group_2))
          else:
            out = out + "\n"
            #pass

        if match_obj2:
          linetype = 2
          group_1 = match_obj2.group(1)
          group_2 = match_obj2.group(2)
          #new value: 55,
          #print lines[ln-1],
          logon = compile_obj4.search(lines[ln-1])
          a = group_1.split('\\')
          try:
            out = out + "-->%s, [%s] - %s [%s], %sControlWord" %(logon.group(1), group_2, a[0], a[1], group_1)
            rt = cw.plc(int(group_2))
            out = out +  rt
          except:
            pass

        if linetype == 0:
          if line.count('value')>0:
            #print line
            pass
          sval = compile_setval.search(line)
          if sval:
            #print line
            out = out + line


        i = i +1
        ln = ln + 1
        #if i > 10:
        #  break
      self.loglines = out.split('\n')

      #self.color(loglines, mihost)




if __name__ == '__main__':


    for mihost in ['37750']:  #reader:  #37450 fcecspmesweb02,,('fcecsdmesapp01',),('fcecspmesapp02',)
        #print (mihost)
        #print strftime('%Y-%m-%d %H:%M:%S', localtime())
        ws = '37750'

        mila = MILogAnalyzer(mihost, ws)

        print dir(mila.__init__)

        """
        mila.main()
        #mila.color()
        lines = mila.linesReverse()
        for line in lines:
            print line
        """







