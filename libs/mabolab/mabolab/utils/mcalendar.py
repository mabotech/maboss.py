# -*- coding: UTF-8 -*-
import logging
import itertools
import time

import calendar
import datetime

import lunarcalendar

log = logging.getLogger(__name__)

class MCalendar:

  def __init__(self, year, firstweekday = 0):
    self.year = year
    self.firstweekday = firstweekday
    self.cwd = self.cycleweekdays(self.firstweekday)
    self.lunar = lunarcalendar.LunarCalendar()

    self.weekdays = ['一','二','三','四','五','六','日']

    self.LMonth = [
      '正月', '二月', '三月', '四月', '五月', '六月',
      '七月', '八月', '九月', '十月', '十一月', '腊月']

    self.LDay = [
      '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
      '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']

  def cycleweekdays(self, index=0):
    #iterable = ['M','T','W','T','F','S','S']
    iterable = ['一','二','三','四','五','六','日']
    saved = []
    length = len(iterable)
    iterable.extend(iterable)
    for i in range(0, length):
      yield iterable[i+index]
      saved.append(iterable[i+index])
    while saved:
        for element in saved:
              yield element

  def getMonthDaysText(self, thismonth):

    monthdays = calendar.Calendar(self.firstweekday).itermonthdates(self.year, thismonth)

    ct = itertools.count(1)

    for d in range(0, 7):
      print "  %s   " %(self.cwd.next()),
    print
    for date in monthdays:
      #weekday =self.cwd.next()
      if date.year != self.year or date.month != thismonth:
        #print "      | ",
        print "  %2d  | " %(date.day),
      else:
        if date == date.today():
          print "today | ",
        else:
          print "  %2d  | " %(date.day),
      if ct.next()%7==0:
        print "\n"

  def getMonthDaysHTML(self, thismonth):

    monthdays = calendar.Calendar(self.firstweekday).itermonthdates(self.year, thismonth)
    ct = itertools.count(1)
    html =  """<table class="month" ><tr><td colspan="7" align="center"> %s - %s </td></tr>""" %(self.year, thismonth)
    html = html + "<tr>"
    for d in range(0, 7):
      html = html + "<td class=\"h\">%s</td>" %(self.cwd.next())
    html = html + "</tr>"
    lunarMonthDates = self.lunar.getLunarMonthDate(self.year, thismonth)
    for date in monthdays:
      lc = ct.next()
      if lc%7==1:
        html = html +  "<tr>"
      if date.year != self.year or date.month != thismonth:
        html = html + "<td>&nbsp;</td>"
      else:
        #if date == date.today():
        #  print "<td>today</td> ",
        #else:
        ymd = "%d%02d%02d"%(date.year, date.month, date.day)
        #(yy,mm,dd,ll) = self.lunar.getLunarDate(date.year, date.month, date.day)

        (yy,mm,dd,ll) = lunarMonthDates.next()

        if dd == 1:
          lunar = "%s" %(self.LMonth[mm-1])
          if ll == 1:
            lunar = "闰" + lunar
        else:
          lunar = "%s" %(self.LDay[dd-1])

        html = html + '<td id="d%s" class="line"><em><span>%2d <br/> %s</span></em></td>' %(ymd, date.day, lunar)
      if lc%7==0:
        html = html + "</tr>\n"
    html = html + """</table>\n"""
    return html

  def getMonthDaysDict(self, thismonth):


    mddict = {}

    monthdays = calendar.Calendar(self.firstweekday).itermonthdates(self.year, thismonth)
    ct = itertools.count(1)
    html =  """<table class="month" ><tr><td colspan="7" align="center"> %s - %s </td></tr>""" %(self.year, thismonth)
    mddict['year'] = self.year
    mddict['month'] = thismonth

    html = html + "<tr>"
    wdays = []
    for d in range(0, 7):
      wdays.append(self.cwd.next())


    mddict['week'] = self.weekdays #wdays

    lunarMonthDates = self.lunar.getLunarMonthDate(self.year, thismonth)
    oneweek = []
    weeks = []
    for date in monthdays:
      lc = ct.next()
      if lc%7==1:
        pass
      if date.year != self.year or date.month != thismonth:
        oneweek.append(('',''))
      else:
        (yy,mm,dd,ll) = lunarMonthDates.next()

        #log.debug((yy,mm,dd,ll))

        if dd == 1:
          lunar = "%s" %(self.LMonth[mm-1])
          if ll == 1:
            lunar = "闰" + lunar
        else:
          lunar = "%s" %(self.LDay[dd-1])
        oneweek.append((date.day, lunar))
      if lc%7==0:
        weeks.append(oneweek)
        oneweek = []

    mddict['weeks'] = weeks
    return mddict

  def getYearDateHTML(self):
    for i in range(1,13):
      html =  self.getMonthDaysHTML(i)
      yield html

def test():
  mc = MCalendar(2009)
  f = file('calendar002.html','w')
  h =  """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>TheyHope.com</title>
<meta  http-equiv="content-type" content="text/html; charset=utf-8"  />
<link rel="shortcut icon" href="/favicon.ico"/>
<link href="calendar.css" media="screen" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/javascripts/jquery_all.js" charset="utf-8"></script>
</head>
<body>"""

  t = """</body></html>
    """
  f.write(h)
  for i in mc.getYearDateHTML():
      f.write(i)
      #pass
  f.write(t)
  f.close()

if __name__ == "__main__":
    t1 = time.time()
    #for i in range(0,100):  #100 -> 2.4, no IO, 1.4
    test()
    t2 = time.time()
    print t2 - t1








