# -*- coding: utf-8 -*-

import os

from subprocess import Popen, PIPE

import base64

import logging
import logging.config 

logger = logging.getLogger(__name__)



def open_cmd(cmd):
    
    logger.debug(cmd)
    p1 = Popen(cmd, shell=True, stdout=PIPE)
    
    output = p1.communicate()[0]
    
    logger.debug("output"+output)
    
    
    
def open_cmd2(cmd):
    
    
    #print cmd
    logger.debug(cmd)
    
   
    rt = os.popen(cmd)
    rtn_info = rt.read()
    logger.debug(rtn_info)
   
    
def get_token(s):
    
    return base64.b64decode(s)
    
def gen(s):
    s = base64.b64encode(s)
    print s
    
    s1 = get_token(s)
    
    print s1
    
    
if __name__ == "__main__":
    
    gen("Administrator B0st0nP")
