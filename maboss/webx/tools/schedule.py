# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence

from sqlalchemy import Column

from sqlalchemy import BigInteger, Integer, SmallInteger
from sqlalchemy import DateTime, Float, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class Schedule(Base, ColumnMixin):
    
    __tablename__ = 'schedule'
    
    id  = Column( BigInteger, primary_key=True )
    cron  =   Column( Unicode(200) )  # NVARCHAR
    name  =   Column( Unicode(40) )  # NVARCHAR
    operation  =   Column( Unicode(40) )  # NVARCHAR
    sch_type  =   Column( SmallInteger )  # SMALLINT
    interval  =   Column( Float )  # FLOAT
    parameters  =   Column( Unicode(2000) )  # NVARCHAR
    status  =   Column( Integer )  # TINYINT


    def __init__(self, cron, name, operation, sch_type, interval, parameters, status, createdby):
        """init"""
        
        self.cron  = cron
        self.name  = name
        self.operation  = operation
        self.sch_type  = sch_type
        self.interval  = interval
        self.parameters  = parameters
        self.status  = status

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<Schedule(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
            % (self.id, self.cron, self.name, self.operation, self.sch_type, self.interval, self.parameters, self.status)
