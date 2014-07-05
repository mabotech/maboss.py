
import gevent
import random

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(random.randint(0,5)*0.1)
    try:
        print('Task', pid, 'done')
        
        if pid %3==0:
            raise Exception('asyn')
        print "good"
    except:
        
        print "error"
        
def synchronous():
    for i in range(1,10):
        task(i)

def asynchronous(i):
    
    v = gevent.spawn(task, i) 
    
    #threads = [for i in xrange(20)]
    #gevent.joinall([v])
    #gevent.sleep(random.randint(0,2)*0.001)
    #print "=="

#print('Synchronous:')
#synchronous()

print('Asynchronous:')
import time
t = time.time()
for i in xrange(20):
    asynchronous(i)
    
gevent.sleep(3)
print time.time() - t