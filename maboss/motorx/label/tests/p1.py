
import os, sys

import time

from twisted.internet import reactor, defer

from twisted.internet.threads import deferToThread
deferred = deferToThread.__get__

## example code

def printing_ok(result, i):
    
    print "=="*20
    print i
    print "OK"
    print result

def printing_err(result, i):
    
    print "=="*20
    print i
    print "Err"
    print result
    
    
def running(i):
    "Prints a few dots on stdout while the reactor is running."
    #if i % 3 == 0:
    call_printer(3,i ).addCallback(printing_ok, i).addErrback(printing_err, i)
    sys.stdout.write(".")
    sys.stdout.flush()
    i = i + 1
    reactor.callLater(1, running, i)

@deferred
def call_printer(sec, i):
    "A blocking function magically converted in a non-blocking one."
    print 'start sleep %s' % sec
    if i %2 == 0:
        raise Exception("error")
    time.sleep(sec)
    print '\nend sleep %s' % sec
    return "sleep ok"

if __name__ == "__main__":
    
    
    
    reactor.callLater(1, running, 1)
    reactor.callLater(16, reactor.stop)
    
    reactor.run()