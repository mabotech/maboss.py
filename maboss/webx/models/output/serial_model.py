# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class SerialModel(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_serial_model'
    
    id  = Column(Integer,  primary_key=True)
    engineserial  = Column(Unicode(40))     # NVARCHAR2       
    model  = Column(Unicode(40))     # NVARCHAR2       


    def __init__(self, engineserial, model, createdby):
        """init"""
        
        self.engineserial  = engineserial
        self.model  = model

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<SerialModel(%s, '%s', '%s')>" \
            % (self.id, self.engineserial, self.model)
