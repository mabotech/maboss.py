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


class Weixin(Base, ColumnMixin):
    
    __tablename__ = 'mt_t_weixin'
    
    id                     =  Column( BigInteger, primary_key=True )
    msgclass               =  Column( Unicode(20) )  # NVARCHAR
    msgid                  =  Column( Unicode(40) )  # NVARCHAR
    msgtype                =  Column( Unicode(40) )  # NVARCHAR
    fromusername           =  Column( Unicode(60) )  # NVARCHAR
    tousername             =  Column( Unicode(60) )  # NVARCHAR
    createtime             =  Column( BigInteger )  # BIGINT
    content                =  Column( Unicode(2000) )  # NVARCHAR


    def __init__(self, msgclass, msgid, msgtype, fromusername, tousername, createtime, content, createdby):
        """init"""
        
        self.msgclass  = msgclass
        self.msgid  = msgid
        self.msgtype  = msgtype
        self.fromusername  = fromusername
        self.tousername  = tousername
        self.createtime  = createtime
        self.content  = content

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return "<Weixin(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
            % (self.id, self.msgclass, self.msgid, self.msgtype, self.fromusername, self.tousername, self.createtime, self.content)
