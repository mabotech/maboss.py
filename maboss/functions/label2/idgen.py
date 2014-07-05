

from time import time

import base64, M2Crypto

import hashlib

import uuid

from uuid import uuid4

import os

def idgen1(esn):
  
    m = hashlib.md5()
    m.update(esn)
    x =  m.hexdigest()   
    m.update(x)
    return m.hexdigest()   

def idgen2(esn):    
    return  str( uuid.uuid3(uuid.NAMESPACE_DNS, esn) )
    
def idgen3(l=12):
    s = base64.b64encode(os.urandom(l)) 
    return s.replace('=', '')

def idgen4(num_bytes = 16):
    #s = base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))
    #return s.replace('=', '')
    #
    pass
    
def idgen5():
    return uuid4().hex

def main():
    
    v = idgen1('90001011')
    
    print v
    
    print len(v)
    
    
    print idgen2('esn0011000')
    print idgen3()
    #print idgen4()
    print idgen5()
    
if __name__ == "__main__":
    

        main()
        pass
        