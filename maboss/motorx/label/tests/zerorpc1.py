
import time

import gevent

import zerorpc

endpoint = 'tcp://127.0.0.1:6234'

class MySrv(zerorpc.Server):

    def lolita(self, i):
        return 42 + i


def main():
    
    
    
    srv = MySrv()
    srv.bind(endpoint)
    gevent.spawn(srv.run)
    
    t = time.time()
    client = zerorpc.Client()
    client.connect(endpoint)

    print client.lolita(121)
    
    t2 = time.time()
    
    print t2-t


main()    
