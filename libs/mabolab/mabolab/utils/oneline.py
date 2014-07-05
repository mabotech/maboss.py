# -*- coding: utf-8 -*-

import logging
from time import time, strftime, localtime

from kserver.model import meta

from time import time, mktime

import colorlib

log = logging.getLogger(__name__)

def fractSec(s):
   years, s = divmod(s, 31556952)
   min, s = divmod(s, 60)
   h, min = divmod(min, 60)
   d, h = divmod(h, 24)
   return [years, d, h, min, s]

def  getlist(arr):
  if arr[0]==0:
    arr.pop(0)
    if len(arr) == 0:
      return [0]
    return getlist(arr)
  else:
    return arr
    
    
def seccvt(sec):
  x = fractSec(sec)    
  x = getlist(x)
  y = ''
  i = 0
  u = ['S','M','H','D','Y']
  for item in range(0,len(x)):
    y =  "%s%s %s"%(x.pop(),u[i], y)
    i = i + 1
    #print y
  return y.strip()

class OneLine:
    """
    todo: add schema for all sql files
    """

    def __init__(self):


        #dbc = DBC()
        self.color = colorlib.Color()
        #self.curs = dbc.getCurs()

        #self.out = open('ws.dot', 'w')

        self.gp = {}

        self.gpr = {}

        self.pt = {}

        self.free = []
        
        self.workstations = []

        self.group()

        self.wspath()


    def __del__(self):
        #self.out.close()
        pass

    def group(self):
        sql ="""
        select fk_area_id, workstation from workstations where fk_area_id is not null
        """
        rtn = meta.Session_post.execute(sql)
        data = rtn.fetchall()
        for item in data:
            #print item
            self.workstations.append(item[1])
            if item[0] in self.gp:
                #print item
                pass
                self.gp[item[0]].append(item[1])
            else:
                self.gp[item[0]] = []
                self.gp[item[0]].append(item[1])

        self.workstations.sort()
        for item in data:
            self.gpr[item[1]] = item[0]

    def do(self, esns, stations):
        g =  """
     digraph G {
     nodesep=.03;
     rankdir=LR;
     labelloc=t;
     label="Line: 38";
     nodesep=.05;
      node [shape=record,width=.1,height=.1];
     line38[shape=plaintext, label=<<table border="0" cellborder="1" cellspacing="0" >
        """
        
        for station in stations:# self.workstations:#stations:
            if station in esns:
                g = g + """<tr><td port="%s" height="60" bgcolor="lightblue">%s(%s)</td></tr>""" %(station, station, len(esns[station]))

        g = g+"""</table>>]\n"""
        
        for station in stations:


            if station in esns:  
                g = g + """%s[shape=plaintext, label=<<table border="0" cellborder="1" cellspacing="0"><tr>"""%(station)
                ti = 0
                for esn in esns[station]:
                    duration = time() - mktime ( esn[2].timetuple( ) ) - 8* 60 * 60
                    if duration <0:
                        duration =  time() - mktime ( esn[2].timetuple( ) ) 
                    cl = self.color.getColor(duration)
                    ti == ti + 1
                    #if ti % 10 == 0:
                    #    g = g + """<td bgcolor="lightblue" href="#" title="title">%s<br/>%s</td>"""%(esn[0], esn[4])
                    #else:
                    title = "%s -- %s"%(esn[0], esn[4])
                    g = g + """<td bgcolor="#%s" target="_blank" href="/flow/engine/%s" title="%s"> <font color="blue">%s</font> (%s)<br/><font color="blue">%s</font>[%s]</td>"""%(cl, esn[0], title, esn[0],esn[3], esn[4][:-6], seccvt(int(duration)))
                    #pass
                g = g + """</tr></table>>]\n"""
                
                g = g + """line38:%s -> %s[headlabel="%s" labeldistance="3.0"]\n""" %(station, station, station)
                
        g = g + """}"""
        
        return g
        
    def do1(self, esns, stations):
        
        # node[style=filled, fillcolor=lightgray, color=black, fontsize=8, shape=box];
        g =  """
    graph G {
rankdir = LR;
fontsize=16;
labelloc=t;
label="Line: 38"
color = red;
node[style=filled, fillcolor=lightgray, color=lightgray, fontsize=8, shape=box];
edge[arrowhead=normal,color=blue, fontsize=10];

        """ ### %(stations[0][0])

        """
        for station in stations:
            s = float(station[2])
            r = float(station[3])
            t = r * 81/s
            cl = self.color.getColor(t)
            g = g + '''%s[style=filled, fillcolor="#%s", color=black, fontsize=8, shape=box, label="%s\\n%s/%s"];\n''' %(station[1], cl, station[1],station[3],station[4])
        """
        for item in stations:


            if item in esns:
                tab =  """<table border="0" cellborder="1" cellspacing="0" ><tr><td colspan="%s">%s</td></tr><tr>"""%(len(esns[item]), item)

                i = 0
                for esn in esns[item]:
                    i = i + 1

                    duration = time() - mktime ( esn[2].timetuple( ) ) - 8* 60 * 60
                    if duration <0:
                        duration =  time() - mktime ( esn[2].timetuple( ) ) 
                    cl = self.color.getColor(duration)
                    tab = tab +  '''<td href="/flow/engine/%s" title="%s" target="_blank" port="%s" bgcolor="#%s">%s<br/>(%s/%s)</td>'''%(esn[0], esn[0], i, cl, esn[0], seccvt(int(duration)),esn[3])
                tab = tab +  """</tr></table>"""

                g = g + """%s[shape=plaintext, label=<%s>];\n"""%(item, tab)
            else:
                g = g + "%s;" %(item)

        for item in self.gp:
            #print item
            g = g +'''subgraph cluster_%s {\n''' %(item)
            g = g +'''style= "dashed";\n'''
            g = g + '''color=purple; \n'''
            g = g + '''label="zone %s"; \n''' %(item)
            if item > 10:
                for p in self.pt[item]:
                    x = p.split('--')
                    g =  g + "%s -- %s[arrowtail=normal, arrowhead= none];\n" %(x[1], x[0])
            else:
                for p in self.pt[item]:
                    g =  g + p + ";\n"
                for one in self.gp[item]:
                    #print one
                    pass
            g = g + '''}\n'''
        #print "/* ----- */"
        for item in self.free:
            g = g + item + '\n'

        g = g +'''
        { rank = same;37200;36000;35200;46000;47150;48600;50000;}


}
        '''
        #self.out.write(g)


        return g

    def wspath(self):
        sql ="""
        select wsfrom, wsto from ws_paths
        """
        rtn = meta.Session_post.execute(sql)
        data = rtn.fetchall()
        for item in data:
            #print item
            x =   self.gpr[item[0]]
            y =   self.gpr[item[1]]
            #print x,y
            p  = '%s --  %s'%(item[0],item[1])
            if x == y:
                if x in self.pt:
                    self.pt[x].append(p)
                else:
                    self.pt[x] = []
                    self.pt[x].append(p)
            else:
                if x - 12 ==0 or y - 15 ==0 or  x - 15 ==0 or y - 12 ==0:
                    p  = '%s -- %s[arrowtail=normal, arrowhead= none]'%(item[1],item[0])
                    self.free.append(p)
                else:
                    self.free.append(p)

            pass
        #print self.pt
