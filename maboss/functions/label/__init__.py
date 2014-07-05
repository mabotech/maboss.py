# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

if __name__ == "__main__":
    from mabolab.database.config import LOGGING
    logging.config.dictConfig( LOGGING )

log = logging.getLogger(__name__)

from msgpack import packb, unpackb

#===============================================================================

from field_query import FieldQuery

from label_print import LabelPrint


class Demo(object):
    
    pass


def print_label(args):
    """
    bla
    input:
    {'workstation':'workstation'}
    output:
    {'data','data'}
    bla
    """
    
    input = unpackb(args)
    
    workstation = input['workstation']
    
    lp = LabelPrint()
    
    rtn =  lp.printit(workstation)
    
    return rtn
    
def query_printer(args):
  
    lp = LabelPrint()
    
    input = unpackb(args)
    
    workstation = input['workstation']
    
    rtn = lp.query_status(workstation)
    
    return rtn
            
            
if __name__ == '__main__':
    
    args = packb({'workstation' : 62300 } )
    
    print_label(args)
    
    query_printer(args)

    