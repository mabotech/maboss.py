# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class ProductionLicHis(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_production_lic_his'
    
    id  = Column(Integer,  primary_key=True)
    production_license  = Column(Unicode(40))     # NVARCHAR2       


    def __init__(self, production_license, createdby):
        """init"""
        
        self.production_license  = production_license

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<ProductionLicHis(%s, '%s')>" \
            % (self.id, self.production_license)
