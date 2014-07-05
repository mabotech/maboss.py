# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class CertificatePrintm(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_certificate_printm'
    
    id  = Column(Integer,  primary_key=True)
    serialno  = Column(Unicode(40))     # NVARCHAR2       
    certificate_no  = Column(Unicode(60))     # NVARCHAR2       
    validation_code  = Column(Unicode(80))     # NVARCHAR2       
    model  = Column(Unicode(40))     # NVARCHAR2       
    engineserial  = Column(Unicode(40))     # NVARCHAR2       
    inspection_date  = Column(Unicode(12))     # NVARCHAR2       
    printing_workstation  = Column(Unicode(10))     # NVARCHAR2       
    reason  = Column(Unicode(2000))     # NVARCHAR2       
    status  = Column(Integer) 


    def __init__(self, serialno, certificate_no, validation_code, model, engineserial, inspection_date, printing_workstation, reason, status, createdby):
        """init"""
        
        self.serialno  = serialno
        self.certificate_no  = certificate_no
        self.validation_code  = validation_code
        self.model  = model
        self.engineserial  = engineserial
        self.inspection_date  = inspection_date
        self.printing_workstation  = printing_workstation
        self.reason  = reason
        self.status  = status

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<CertificatePrintm(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
            % (self.id, self.serialno, self.certificate_no, self.validation_code, self.model, self.engineserial, self.inspection_date, self.printing_workstation, self.reason, self.status)
