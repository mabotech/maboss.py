


import gevent

import time



def doit(i):
    
    print "do it:%s" % (i)
    gevent.sleep(2)
    print "done:%s" %(i)
    
    
t2 = time.time()

threads = {}

for i in range(5):
    t = gevent.spawn(doit, i)
    threads[i] = t
    #print dir(t)
    
gevent.sleep(1)

print threads

print threads[3].dead
threads[3].kill()
print threads[3].dead
del threads[3]
threads[2].kill()
print threads
#gevent.sleep(3)
print time.time() - t2
for i in threads:
    print threads[ i ].dead
#print t
gevent.sleep(3)
print time.time() - t2
for i in threads:
    print threads[ i ].dead
