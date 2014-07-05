
import os, sys

import time

from twisted.internet import reactor, defer

from twisted.internet.threads import deferToThread

def sendLine(line):
    print line

def lineReceived(line):
    sendLine('server: '+line)
    d = mySleep(1)
    d.addCallback(sendLine, 'Suc').addErrback(sendLine, 'Err')
    reactor.callLater(1, lineReceived,' -1')

def mySleep(second):
    d = defer.Deferred()
    d.deferToThread(time.sleep, 2)
    return d 


reactor.callLater(1, lineReceived, '1')
reactor.callLater(16, reactor.stop)

reactor.run()