
import time
from time import localtime, strftime

from gevent.server import StreamServer

def handle(socket, address):
    
    try:
        socket.send("Hello from a telnet!\n")
        socket.send(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        socket.send("\n")
        for i in range(5):
            socket.send(str(i) + '\n')
    except Exception, e:        
        pass        
    finally:
        print "close"
        socket.close()

server = StreamServer(('127.0.0.1', 5001), handle)

server.serve_forever()