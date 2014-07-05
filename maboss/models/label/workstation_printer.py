# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class WorkstationPrinter(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_workstation_printer'
    
    id  = Column(Integer,  primary_key=True)
    workstation  = Column(Unicode(40))     # NVARCHAR2       
    printer_name  = Column(Unicode(40))     # NVARCHAR2       
    ip_address  = Column(Unicode(80))     # NVARCHAR2       
    spool_address  = Column(Unicode(60))     # NVARCHAR2       
    template_path  = Column(Unicode(80))     # NVARCHAR2       


    def __init__(self, workstation, printer_name, ip_address, spool_address, template_path, createdby):
        """init"""
        
        self.workstation  = workstation
        self.printer_name  = printer_name
        self.ip_address  = ip_address
        self.spool_address  = spool_address
        self.template_path  = template_path

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<WorkstationPrinter(%s, '%s', '%s', '%s', '%s', '%s')>" \
            % (self.id, self.workstation, self.printer_name, self.ip_address, self.spool_address, self.template_path)
