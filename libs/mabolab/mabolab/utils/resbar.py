#import logging

import numpy as np

import matplotlib

matplotlib.use('Agg')
matplotlib.rcParams['legend.shadow'] = True
matplotlib.rcParams['figure.subplot.left'] = 0.15
matplotlib.rcParams['figure.subplot.top'] = 0.8
matplotlib.rcParams['figure.subplot.bottom'] = 0.2
#matplotlib.rcParams['xtick.direction'] = 'out'
#matplotlib.rcParams['xtick.major.size'] = 25
#matplotlib.rcParams['axes.edgecolor'] = "blue"
#matplotlib.rcParams['axes.labelcolor'] = "blue"
#matplotlib.rcParams['xtick.color'] = "blue"
matplotlib.rcParams['legend.fontsize'] = 'small'
matplotlib.rcParams['legend.loc'] = 'best'


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


#from cStringIO import StringIO


class Plot:
  
    def __init__(self):
      pass

    def gen(self, cpu, mem, disk, net, servers):
      fig = Figure()
      canvas = FigureCanvas(fig)
      ax = fig.add_subplot(111) #, frameon=False

      #ax.axis["top"].set_visible(False)
      

      #log.debug(dir(ax))
      

      
      base = []
      for i in range(0, len(cpu)):
          base.append(cpu[i] + mem[i])
      base = tuple(base)
      
      base2 = []
      for i in range(0, len(cpu)):
          base2.append(base[i] + disk[i])
      base2 = tuple(base2)      
      
      
      

      N = len(cpu)
      ind = np.arange(N)    # the x locations for the groups
      
      c_cpu = '#FF4500'
      c_mem = '#AFEEEE'
      c_disk = '#B500B5'
      c_net = '#1E90FF'
      
      ones = np.ones(N)
      ax.plot(np.array(ones)*30, '--')
      
      ax.plot(np.array(cpu)+50,   color=c_cpu)  # o-,*-, +-, <-
      ax.plot(np.array(mem)*0.5+50,   color=c_mem)
      ax.plot(np.array(disk)+50,  color=c_disk)
      #ax.plot(np.array(net)+50,  color=c_net)
      #log.debug(ind)
      width = 0.80       # the width of the bars: can also be len(x) sequence

      p1 = ax.bar(ind, cpu, width, color=c_cpu, edgecolor =c_cpu )
      p2 = ax.bar(ind, mem, width, color=c_mem, edgecolor=c_mem, bottom=cpu )
      p3 = ax.bar(ind, disk, width, color=c_disk, edgecolor=c_disk, bottom=base )   
      p4 = ax.bar(ind, net, width, color=c_net, edgecolor=c_net,  bottom=base2 )  
      
      ax.set_xticks(ind + width * 0.5)
      ax.set_xticklabels( servers, multialignment='right', position=(0,0) ) 
      labels = ax.get_xticklabels()
      n = 0
      for label in labels:
          k = 0.1 * (n%3+1)
          n = n + 1
          label.set_rotation(35 ) 
          label.set_ha('right')
          text = label.get_text()
          if text.count('MES')>0:
            if text[:1] == 'P':
                if text.count('OPC')>0:
                    label.set_color('#800080')
                else:
                    label.set_color('red')
            else:
                label.set_color('blue')
          #label.set_position((0, 0.1  ))
          label.set_size('x-small')
      #log.debug(dir(label))
      ax.set_title('Servers Resource Utilization')
      
      #ax.grid(True)

      #ax.set_xlabel('Servers')
      ax.set_ylabel('Utilization')

      ax.legend( (p1[0], p2[0],p3[0], p4[0]), ('CPU', 'MEM','DISK','NET'))
      #ax.legend( (p1[0], p2[0],p3[0], p4[0]), ('CPU', 'MEM','DISK','NET'),loc=(0.05,0.7))
      #f = file('a.png','w')
      #canvas.print_figure(f)
      fig.savefig("C:\\opt\\KServer\\kserver\\public\\report\\res.png")
      #f.close()


if __name__ == "__main__":
  p = Plot()
  cpu = (20, 30, 30, 35, 27,20, 35, 30, 35, 27,20, 35, 30, 35, 27,20, 35, 30, 35, 27,20, 35)
  mem = (10, 30, 34, 20, 25,25, 32, 34, 20, 25,25, 32, 34, 20, 25,25, 32, 34, 20, 25,25, 32)
  net = (30, 30, 34, 1, 2,25, 32, 34, 4, 25,25, 5, 34, 20, 25,6, 32, 2, 11, 3,5, 4)
  p.gen(cpu, mem, net)
