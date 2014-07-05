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

from mabolab.common.singleton import Singleton
from mabolab.core.base import Base

from idgen import idgen3

if __name__ == '__main__':
    from flask.config import Config
    settings = Config("" )
    settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')
    settings['APP_NAME'] = "certificate_label"
    base = Base( settings)
    db = base.get_db("oracle") 

else:   
    base = Base()
    db = base.get_db("oracle") 
    settings = base.get_config()
    

from maboss.models.label.certificate import Certificate

class CertificateData(Singleton):
    """
    
    """
    def __init__(self):
        
        super(CertificateData, self).__init__()   
        
   
    def save(self, serialno, certificate_no, validation_code, model, engineserial, inspection_date, status, production_license, createdby):
        
        t = time.time()
        cert = Certificate(serialno, certificate_no, validation_code, model, engineserial, inspection_date, status, production_license, createdby)
        
        try:
            db.session.add(cert)
            db.session.commit()
            return cert.id
        except Exception, e:
            
            raise Exception(e.message)
            
            db.session.rollback()            
            #log.error(e.message)
            return 0
        
    
    
    
def test():

    cd=  CertificateData()

    print cd.save()
    

    
if __name__ == "__main__":    
    test()