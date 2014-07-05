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


class Certificate(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_certificate'
    


    def __init__(self, , createdby):
        """init"""
        

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<Certificate(%s, )>" \
            % (self.id, )
