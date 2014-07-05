# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

class ColumnMixin(object):
    
    referenceid = Column(Integer)
    
    lastupdateon =  Column(DateTime, default=datetime.now())
    lastupdateby = Column(String(40))
    
    createdby = Column(String(40))
    createdon = Column(DateTime, default=datetime.now())
    
    active = Column(Integer, default=1)
    
    rowversionstamp = Column(Integer, default=1) 