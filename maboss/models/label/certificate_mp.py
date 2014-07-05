# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin


class CertificateMP(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_certificate_mp'
    
    id  = Column(Integer, Sequence('mt_user_id_seq'), primary_key=True)
    serialno  = Column(Unicode(40))     # NVARCHAR2       
    certificate_no  = Column(Unicode(60))     # NVARCHAR2       
    validation_code  = Column(Unicode(80))     # NVARCHAR2       
    model  = Column(Unicode(40))     # NVARCHAR2       
    so_no  = Column(Unicode(40))     # NVARCHAR2       
    reason  = Column(Unicode(2000))     # NVARCHAR2       
    status  = Column(Integer) 


    def __init__(self, serialno, certificate_no, validation_code, model, so_no, reason, status):
        self.serialno  = serialno
        self.certificate_no  = certificate_no
        self.validation_code  = validation_code
        self.model  = model
        self.so_no  = so_no
        self.reason  = reason
        self.status  = status

        self.createdon = datetime.now()
        self.active = 1
        self.rowversionstamp = 1

