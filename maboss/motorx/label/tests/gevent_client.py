
import sys
sys.setrecursionlimit(40)

import time
from time import strftime, localtime

import gevent

from gevent import socket

from msgpack import packb, unpackb

#server = SimpleServer(('127.0.0.1', 0))
#server.start()

def query(i):

    t = time.time()

    try:
        client = socket.create_connection(('127.0.0.1', 5001))
        
    except Exception, e:
        
        print ">>"*20
        print e.message
        
        return ""
    
    v = {'dd_%s'%(i):'abc12333:'+ str(t)} 
    
    print v
    
    client.send( packb(v))

    y = client.recv(10240)

    print unpackb(y)

    print time.time() - t


    #print dir(client)

    #client.send('0')

    #y = client.recv(10240)

    #print "[%s]"%(y)
    
    gevent.sleep(0)
    
    client.close()



    #response = client.makefile().read()
    #print response
    #server.stop()

def loop():
    
    print "=="*20
    print strftime("%Y-%m-%d %H:%M:%S", localtime())
    print "=="*20
    print "in loop\n"
    
    try:
        for i in xrange(3):
            
            gevent.spawn(query, i) 
            
    except Exception, e:

        print e.message

    gevent.sleep(1) #joinall(v)
    
    gevent.spawn(loop).join() #waiting the loop finish


def run():
    
    print "run"

    loop()
    
    
if __name__ == '__main__':
    
    run()
    #gevent.sleep(100)
    
    