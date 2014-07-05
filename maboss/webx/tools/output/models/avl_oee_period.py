# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence

from sqlalchemy import Column

from sqlalchemy import BigInteger, Integer, SmallInteger
from sqlalchemy import DateTime, Float, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base


class Avl_oee_period(Base):
    
    __tablename__ = 'avl_oee_period'
    
    avl_oee_period_id      =  Column( BigInteger, primary_key=True )
    station                =  Column( Unicode(50) )  # character varying
    start_time             =  Column( Unicode(30) )  # character varying
    end_time               =  Column( Unicode(30) )  # character varying
    test9_count            =  Column( BigInteger )  # bigint
    test9_success          =  Column( BigInteger )  # bigint
    test30_count           =  Column( BigInteger )  # bigint
    test30_success         =  Column( BigInteger )  # bigint
    runningtime            =  Column( Float )  # double precision
    availablerate          =  Column( Float )  # double precision
    date_                  =  Column( Date )  # date
    active                 =  Column( Integer )  # smallint
    createdon              =  Column( Datetime )  # timestamp without time zone
    createdby              =  Column( Unicode(30) )  # character varying
    lastupdatedby          =  Column( Unicode(30) )  # character varying
    lastupdateon           =  Column( Datetime )  # timestamp without time zone
    rowversionstamp        =  Column( Integer )  # integer


    def __init__(self):
        """init"""
        pass



    def __repr__(self):
        return "<Avl_oee_period(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
            % (self.id, self.avl_oee_period_id, self.station, self.start_time, self.end_time, self.test9_count, self.test9_success, self.test30_count, self.test30_success, self.runningtime, self.availablerate, self.date_, self.active, self.createdon, self.createdby, self.lastupdatedby, self.lastupdateon, self.rowversionstamp)
