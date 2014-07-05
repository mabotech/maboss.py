


# make a horizontal bar chart
import matplotlib

matplotlib.use('Agg')

matplotlib.rcParams['figure.figsize'] = (6.4,3.2)
matplotlib.rcParams['figure.dpi'] = 96
matplotlib.rcParams['axes.edgecolor'] = '#B2B2B2'

import matplotlib.pyplot as plt

from pylab import *

import numpy as np

data = [1,2]

d = np.array(data)

print d, type(d)


val = 3+10*rand(12)    # the bar lengths

print type(val)

print val

pos = arange(12)+.5    # the bar centers on the y axis

print type(pos)

print pos

figure(1)
barh(pos,val, align='center',  edgecolor='#FFCC99',facecolor='#FFFF66')


hours = arange(12)

#   hours.revise()

yticks(pos, hours)

xlabel('Performance')

title('How fast do you want to go today?')

grid(True)


plt.savefig('hbar01')
