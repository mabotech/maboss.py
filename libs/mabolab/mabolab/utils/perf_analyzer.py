
from itertools import count

from time import strptime, strftime, localtime


from mako.template import Template


def htmlgen(rows, summary):

  out = file("perf001_1.html","w")

  template_file = file("perf.mako","r")

  template_string = ""

  for line in template_file:
      template_string= "%s%s"%(template_string,  line)

  template =  Template(template_string,  default_filters=['decode.utf8'],  output_encoding='utf8')


  output_html = template.render(rows, summary)

  out.writelines(output_html)
  out.close()

def perf(th, tag):

    c = count(0)

    perf = file('FlexNet_PerformanceRolling.log','r')

    format = "%Y-%m-%d %H:%M:%S"

    wsop = 0
    delay = 0

    lwsop = 0
    ldelay = 0

    row = {}
    rows = []

    print strftime(format, localtime())
    xp = 0
    stat = 'n'

    out = file('perf_%s.html'%(tag),'w')
    html = '''
    <html><head>
    <title>performance viewer</title>

    </head>
    <body>
    '''

    table = '''
    <table border="1" align="center">
    <tr  bgcolor="#f1f1f1"><td>Level</td><td>CreatedOn</td><td> durition </td><td>Step</td><td>Function</td></tr>
    '''
    j = 0
    for line in perf:
        i = c.next()
        if i > 1000:
            #break
            pass
        x = line.split('\t')
        if len(x) == 1:
            #print "--------------------"
            pass
        else:
            #print "len:%s"%(len(x))
            t = strptime( x[1].split(',')[0], format)
            #print ">>>>%s,%s" %(xp, int(x[0]))
            #print i, x[0],line,
            if xp < int(x[0]):
                state = 'n'
            else:
                state = 'p'
            xp = int(x[0])

            #print x[1].split(',')[0]

            if t > strptime('2009-07-01 0:0:0', format):
                if float(x[2])<0.05:
                    continue
                j = j + 1
                if line.count(tag) == 1 or tag == "$":
                    wsop = wsop + 1
                    delay = delay +float(x[2])

                if  float(x[2])>th:
                    if line.count(tag) == 1 or tag == "$":
                        lwsop = lwsop + 1
                        ldelay = ldelay +float(x[2])
                    #if state == 'p':

                    color = "FF%02x00" %((255*th) / float(x[2]))
                    if line.count('Step:') == 1:
                        table = table +  """<tr ><td>%s</td><td>%s</td><td>%s</td><td bgcolor="%s">%s</td><td>%s</td></tr>""" %(x[0],x[1],x[2], color,  x[4],'&nbsp;')
                    elif line.count('Function:')  ==1 :
                        table = table +"""<tr ><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td bgcolor="%s">%s</td></tr>""" %(x[0],x[1],x[2],'&nbsp;',color,  x[4])




    summary = """
    <table align = "center", border ="1">
    <tr><td>  total step </td><td> %s </td><td> delay </td><td> %s </td><td> Average </td><td> %2.4f </td></tr>
    <tr><td>long step &gt; %2.2f </td><td>  %s </td><td>  long delay </td><td> %s </td><td> Average </td><td> %2.4f </td></tr>
    </td></tr>
    </table>

    """ %(wsop, delay, delay/wsop, th, lwsop, ldelay, ldelay/lwsop)

    html = html + summary +  table + """</table></body></html>"""

    out.write(html)
    print i, j
    out.close()


if __name__ == "__main__":
    th = 1.0
    tag = 'COB_SO_Lineset_Wraper'#'COB_SO_WS_OPERATION' # 'ReadFromPLC' #'COB_SO_WS_OPERATION',
    tag = '$'
    perf(th, tag)
