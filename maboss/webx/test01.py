

# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
import logging.config
#import profile
import time
from time import strftime, localtime


from datetime import datetime

from Cheetah.Template import Template

from mabolab.core.base import Base

from flask.config import Config

settings = Config("" )

settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')

settings['APP_NAME'] = "mabozen"

base = Base( settings)
db = base.get_db("oracle") 


from models.label.workstation_printer import WorkstationPrinter


def create():
    
    workstation =  'workstation'
    printer_name =  'printer_name'
    ip_address =  '192.168.100.106'
    spool_address =  'spool_address'
    template_path =  'template_path'
    
    try:
        
        wsp = WorkstationPrinter(workstation, printer_name, ip_address, spool_address, template_path, 'MT')
    
        db.session.add(wsp)
    
        db.session.commit()
        
        status = wsp.id
    except Exception, e:
        db.session.rollback()    
        status =  "error"
        raise(Exception(e.message))
        
    return status

def query(id):
    
    wsp = db.session.query(WorkstationPrinter).filter_by(id=id).first()
    
    wsp.ip_address='192.168.1.21'
    
    wsp.lastupdateon = datetime.now()
    
    db.session.add(wsp)

    db.session.commit()
    
    print dir(db.session)
    
    return wsp
    
    

if __name__ == '__main__':
    
    #s = create()
    
    s = query(5)
    
    print s