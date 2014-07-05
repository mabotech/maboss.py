


class TimeLib:
  
  def __init__(self, sec):
    self.sec = sec
  
  def fractSec(self, s):
     years, s = divmod(s, 31556952)
     min, s = divmod(s, 60)
     h, min = divmod(min, 60)
     d, h = divmod(h, 24)
     return [years, d, h, min, s]

  def  getlist(self, arr):
    if arr[0]==0:
      arr.pop(0)
      if len(arr) == 0:
        return [0]
      return self.getlist(arr)
    else:
      return arr
      
      
  def seccvt(self):
    x = self.fractSec(self.sec)    
    x = self.getlist(x)
    y = ''
    i = 0
    u = ['S','M','H','D','Y']
    for item in range(0,len(x)):
      y =  "%s%s %s"%(x.pop(),u[i], y)
      i = i + 1
      #print y
    return y.strip()
    
    
if __name__ == "__main__":
    tl = TimeLib(30550)
    print tl.seccvt()
