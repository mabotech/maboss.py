
import time

from time import strftime, localtime

import gevent

import zerorpc


from msgpack import packb, unpackb


endpoint = 'tcp://127.0.0.1:6234'



class MySrv(zerorpc.Server):

    def lolita(self, i, j):
        v =  unpackb(j)
        
        f = v['func']
        
        print f
        
        if hasattr( self, f ):
            print 'has'
            return self.__call__(f, v['abc'])
            
        
        return 42 + i + v['abc']

    def time(self, i):
        print strftime("%Y-%m-%d %H:%M:%S", localtime())
        return str(i)+' ok'

def main():
    
    
    
    srv = MySrv()
    
    srv.bind(endpoint)
    
    gevent.spawn(srv.run)
    
    t = time.time()
    client = zerorpc.Client()
    client.connect(endpoint)

    j = packb({'abc':10, 'func':'time'})
    
    for i in xrange(1000):
        print client.lolita(111, j)
        gevent.sleep(2)
    
    t2 = time.time()
    
    print t2-t


main()    
