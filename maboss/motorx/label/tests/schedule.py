# -*- coding: utf-8 -*-

import os, sys

import time

import logging
import logging.handlers
import logging.config

#logging.config.fileConfig('c:/mtp/maboss0.1/configuration/logging.ini')

log = logging.getLogger(__name__)

from twisted.internet import reactor
#, defer

from printing import asyn_print
    
def loop(i):
    
    filename = "esn89898809"
    
    if filename != None:

        asyn_print(filename)

    i = i + 1
    
    reactor.callLater(1, loop, i)
    
    
def main():
    
    reactor.callLater(1, loop, 1)
    reactor.callLater(16, reactor.stop)    
    reactor.run()
    
def stop():
     reactor.stop()
    

if __name__ == "__main__":
    
    main()
    
    
    
