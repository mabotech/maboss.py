
from sqlalchemy import create_engine

import xml.parsers.expat

class DB:
  def __init__(self):
    engine = create_engine('oracle://flxuser:flxuser@messpdb')
    self.connection = engine.connect()
    pass

  def execute(self, sql):
    return self.connection.execute(sql)
    
  def getName(self,id):
    
    sql = """select sequenceno, stepname from operation_step where id = %s""" %(id) #stepname
    
    return self.connection.execute(sql).fetchone()
    
class Path:
  
  def __init__(self):
    self.db = DB()
    self.sstate = 0
    self.dstate = 0
    self.anytype = 0
    self.ffov = 0
    self.s = set()
    self.sd = []
    self.pairs  = []
    self.r = {}
    self.currentpath = ''
    pass
    
  def start_element(self, name, attrs):
    #print 'Start element:', name, attrs
    #print name, attrs
    if name == 'SourceStepID':
      self.sstate = 1
    if name == 'DestinationStepID':
      self.dstate = 1   
    if name == 'anyType':
      self.anytype = 1
    if name == 'FlowFunctionOutputValue':
      self.ffov = 1    
    pass
    
  def end_element(self, name):
    #print 'End element:', name
    if name == 'SourceStepID':
      self.sstate = 0
    if name == 'DestinationStepID':
      self.dstate = 0      
    if name == 'anyType':
      self.anytype = 0
    if name == 'FlowFunctionOutputValue':
      self.ffov = 0      
    pass
    
  #anyType
  #FlowFunctionOutputValue
    
  def char_data(self, data):
    #print 'Character data:', repr(data)
    if self.sstate == 1:
      #print data,
      self.sd.append(data)
      self.s.add(data)
    if self.dstate == 1:
      self.sd.append(data)
      self.pairs.append(self.sd)
      self.currentpath = "%s-%s"%(self.sd[0],self.sd[1])
      self.sd = []
      self.s.add(data)
    if self.ffov == 1:
      self.r[self.currentpath] = data
    pass
    
  def __del__(self):
    
    g =  """
  graph G {
   rankdir = TB;
  fontsize=10;
  fontname="simsun.ttc";
  label="Workstation Operation 2.7"
  node[style=filled,color=lightskyblue, fontsize=10, fontname="simsun.ttc" ,shape=box];
  Start[label="Start" color=green shape=diamond]; 
  /* Logout[label="Logout" color=red, shape=ellipse]; */
  Stop[label="Stop" color=red ,shape=ellipse]; 
  edge[arrowhead=normal,fontsize=10, color=blue]; """
    colorlist  = ['darkgreen','red','navy','green','yellow','blue','violet','darksalmon','black','orangered','cyan','darkorange','beige','yellowgreen','black']
  
    for node in self.s:
      if int(node)<1:
        pass
      else:
        g = g + 'Step%s[label="%s - %s"];\n'%(self.db.getName(node)[0],self.db.getName(node)[0],self.db.getName(node)[1])
    
    n = 0
    for item in self.pairs:
      i = n % len(colorlist)
      color = colorlist[i]
      n = n + 1
      #print "%s -> %s" %(item[0],item[1])
      if item[0] == '0':
        g = g + "Start"
      #elif item[0] == '-1':
      #  g = g +  "Logout"
      else:
        g = g +  "Step%s"%(self.db.getName(item[0])[0])
      g = g +  "--"
      if item[1] == '0':
        g = g +  "Start"
      #elif item[1] == '-1':
      #  g = g +  "Logout"        
      elif int(item[1]) < -0:
        g = g +  'Stop[label="%s" ,fontcolor=red,color = red]; \n' %(item[1])
      else:
        r = "%s-%s"%(item[0],item[1])
        if self.r.has_key(r):
          g = g +  'Step%s[label="%s" color = %s];\n'%(self.db.getName(item[1])[0], self.r[r], color)   
        else:
          g = g +  'Step%s[label="%s" color = %s];\n'%(self.db.getName(item[1])[0], '', color)   
    g = g +  "}"
    #print g
    out = file('sub27.dot','w')
    out.write(g)
    out.close()
  
def main():
  p = xml.parsers.expat.ParserCreate()

  path = Path()

  p.StartElementHandler = path.start_element
  p.EndElementHandler = path.end_element
  p.CharacterDataHandler = path.char_data

  #input = file('wp27.xml','r')
  
  input = file('COB_SO_SubAssmMgmt27.xml','r')

  inputxml = ''

  for line in input:
    inputxml = "%s%s"%(inputxml, line)

  p.Parse(inputxml, 1)


if __name__ == '__main__':
  main()
