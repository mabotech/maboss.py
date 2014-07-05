# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

import subprocess

import time

#logging.config.fileConfig('c:/mtp/maboss0.1/configuration/logging.ini')

log = logging.getLogger(__name__)
#from twisted.internet import reactor
from twisted.internet.threads import deferToThread

deferred = deferToThread.__get__


def query_statue():
    
    pass
    
    
def printing(fn):

    text = "abc"

    printer_ip = '127.0.0.1'

    prn_file = 'a1.txt'

    cmd = 'lpr -S %s  -P TLP2844 %s' %(printer_ip, prn_file)

    print cmd

    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    print p1.pid

    print p1.returncode 

    output = p1.communicate()[0]
    
    v = output.strip() 

    print "[%s]" % ( v)
    
    
    if v.count('Error'):
        raise Exception ('printing error:'+v)
        pass
        
def process_ok(result, filename):
    
    print "=="*20
    print filename
    print "good"
    print result
    
    if result == 'm':
        print 'manually'
        pass
    else:
        pass

def process_err(result, filename):
    
    print "=="*20
    print filename
    print "error"
    print result
    
    if result == 'm_err':
        print 'manually / error'
        pass
    else:
        pass

@deferred
def call_printer(fn, i):

    printing(fn)
    
    return "ok"
    
def asyn_print(filename):
    """
    need reactor.run()
    """
    #filename = ""
    i = 0
    call_printer(filename, i ).addCallback(process_ok, filename).addErrback(process_err, filename) 

    
def sync_print(fn):    
    
    try:
        printing(fn)
        process_ok('m', fn)
    except:
        process_err('m_err', fn)
        
    
if __name__ == '__main__':
    
    fn = 'esn8900988'
    
    sync_print(fn)