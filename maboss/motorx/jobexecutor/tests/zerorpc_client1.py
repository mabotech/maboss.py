
import time

from time import strftime, localtime

import gevent

import zerorpc


from msgpack import packb, unpackb


endpoint = 'tcp://127.0.0.1:6234'

def call_rpc(client, i, j):
    
    print client.lolita(i, j), i

def main():


    client = zerorpc.Client() #heartbeat=None
    client.connect(endpoint)

    j = packb({'abc':10, 'func':'time'})
    
    i = 0
    
    while True:
        i = i + 1
        t = time.time()
        
        try:
            
            print strftime("%Y-%m-%d %H:%M:%S", localtime())            
            #call_rpc(client, i, j)
            gevent.spawn(call_rpc, client, i, j )
            
            
        except Exception, e:
            'no heartbeat:restart the server / service'
            print e.message
            pass
            
        gevent.sleep(1)
    
        t2 = time.time()
        
        print t2-t


if __name__ == '__main__':
    main()    