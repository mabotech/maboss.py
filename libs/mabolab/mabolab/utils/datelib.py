
from datetime import timedelta, date



def nextMonth(year, month):
  year = int(year)
  month = int(month) + 1
  if month == 13:
    month = 1
    year = year + 1
  
  return "%s-%s"%(year, month)
  #return (year, month)
  
def previousMonth(year, month):
  year = int(year)
  month = int(month) -1
  if month == 0:
    month = 12
    year = year -1
  return "%s-%s"%(year, month)
  #return (year, month)

def nextDay(ymd):
  (year, month, day) = ymd.split('-')
  x = timedelta(days = 1)
  y = date(int(year), int(month),int(day))
  return y+x
  #print x

def previousDay(ymd):
  (year, month, day) = ymd.split('-')
  x = timedelta(days = 1)
  y = date(int(year), int(month),int(day))
  return y-x
  #print x


def main():
  s = '2010-1'

  y, m = s.split('-')

  year = int(y)
  month = int(m)

  print nextMonth(year, month)
  print previousMonth(year, month)

  d = '2010-08-31'

  print nextDay(d)
  print previousDay(d)
  
if __name__ == "__main__"  :
  main()
