

import sys, signal
from gevent.server import StreamServer
from gevent.pool import Pool
from gevent import monkey

import gevent
import random

from msgpack import packb, unpackb

def signal_handler(signal, frame): 
    sys.exit(0)

class SocketPool(object):

    def __init__(self): 
        self.pool = Pool(1000)

    def listen(self, socket, address):
        
        #while True:
        line =  socket.recv(10240) 
        #print line
        if  line == '0':
            socket.close()
            #break
        gevent.spawn(self.wait, socket, address, line)#.join()
        print 'after spawn'

    def add_handler(self, socket, address):
        
        print address
        
        if self.pool.full(): 
            raise Exception("At maximum pool size")
        else: self.pool.spawn(self.listen, socket, address)

    
    def wait(self, socket,  address, line):
        
        #gevent.sleep(1)
        gevent.sleep(random.randint(0,5)*0.01)
        #print line
        try:
            v = unpackb(line)
            print v
        except Exception, e:
            v = "error"
            print v
            print e
        
        try:
            socket.send( packb({'status':'ok', 'val':v, 'address':address}))
            print 'after sleep'
        except Exception, e:
            print e.message
            
            print 'socket closed'
        finally:
            pass
            #socket.close()

    def shutdown(self): 
        self.pool.kill()

signal.signal(signal.SIGINT, signal_handler)
monkey.patch_all()
sockPool = SocketPool()
server = StreamServer(('127.0.0.1', 5001), sockPool.add_handler)
server.serve_forever()