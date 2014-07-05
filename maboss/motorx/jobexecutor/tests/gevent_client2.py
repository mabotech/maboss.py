

import time
from time import strftime, localtime

import gevent

from gevent import socket

from msgpack import packb, unpackb

#server = SimpleServer(('127.0.0.1', 0))
#server.start()

def query(client, i):

    t = time.time()

    
    
    v = {'dd_%s'%(i):'abc12333:'+ str(t)} 
    
    print v
    
    client.send( packb(v))
    
    while True:
        y = client.recv(10240)
        
        if not y:
            break

        print unpackb(y)

        print time.time() - t


        #print dir(client)

        #client.send('0')

        #y = client.recv(10240)

        #print "[%s]"%(y)
        
        gevent.sleep(0)
    
    #



    #response = client.makefile().read()
    #print response
    #server.stop()

def loop(client):
    
    print "=="*20
    print strftime("%Y-%m-%d %H:%M:%S", localtime())
    print "=="*20
    print "in loop\n"
    for i in xrange(3):

        gevent.spawn(query, client, i) 

    gevent.sleep(3) #joinall(v)
    loop(client)


def run():
    
    client = socket.create_connection(('127.0.0.1', 5001))
    
    print "run"

    loop(client)
    
    client.close()
    
    
if __name__ == '__main__':
    
    run()
    
    