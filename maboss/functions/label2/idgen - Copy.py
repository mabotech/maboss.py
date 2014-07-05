

from time import time

import base64, M2Crypto

import hashlib

import uuid

import os


def idgen3(l=12):
    s = base64.b64encode(os.urandom(l)) 
    return s.replace('=', '')

def idgen4(num_bytes = 16):
    s = base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))
    return s.replace('=', '')
 

def idgen2(esn):    
    return  str( uuid.uuid3(uuid.NAMESPACE_DNS, esn) )


def idgen(esn):
  
    m = hashlib.md5()
    m.update(esn)
    return m.hexdigest()   
    
#import OpenSSL
    
#OpenSSL.rand.bytes(16)

from uuid import uuid4
def new_user_id():
    return uuid4().hex

print new_user_id()
import struct

#print struct.pack('>q', -2**10)
    
from subprocess import Popen, PIPE
IP = "192.168.100.100"

# do_ping(IP)
# The time between ping and arp check must be small, as ARP may not cache long

import re

pid = Popen(["arp", "-a", IP], shell=True, stdout=PIPE)
s = pid.communicate()[0]

print s

mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]    
    
def main():
    
    t = time()
    
    for i in xrange(20):
        esn = str(t+i)
        v = idgen(esn)
    
        print v
    print len(v)
    
    print ""
    
    for i in xrange(20):
        esn = str(t+i)
        v = idgen2(esn)
    
        print v
    print len(v)
    
    print ""
    
    for i in xrange(20):
        esn = str(t+i)
        v = idgen3(16)
    
        print v
    print len(v)
    
    print ""

    for i in xrange(20):
        esn = str(t+i)
        v = idgen4(16)
    
        print v
    print len(v)
    
    print ""    
    
if __name__ == "__main__":
    

        #main()
        pass
        