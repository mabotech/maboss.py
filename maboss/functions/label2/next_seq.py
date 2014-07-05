# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
import logging.config
#import profile
import time
from time import strftime, localtime


from datetime import datetime

from sqlalchemy import String, Integer
from sqlalchemy.sql.expression import text , bindparam, outparam

from mabolab.core.base import Base



from flask.config import Config

settings = Config("" )

settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')

settings['APP_NAME'] = "next_seq"

base = Base( settings)


db = base.get_db("oracle") 


def get_next_seq():
    """ call stored procedure """
    
    sql = """BP_SP_GETNEXTCERTNO (:I_FACILITY, :O_CertNo, :O_Message )"""

    #bind parameters and set out parameters
    params =  [
        bindparam('I_FACILITY', 'GCIC'),
        outparam('O_CertNo', String), 
        outparam('O_Message', String)
        ]  
    
    #call stored procedure
    rtn = db.call_sp(sql, params)
     
    return rtn['O_CertNo']
    
    
if __name__ == "__main__":
    
    print get_next_seq()