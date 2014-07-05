# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

class ColumnMixin(object):
    
    referenceid = Column(Integer)
    
    lastupdateon =  Column(DateTime, default=datetime.now())
    lastupdateby = Column(String(40))
    
    createdby = Column(String(40))
    createdon = Column(DateTime, default=datetime.now())
    
    active = Column(Integer, default=1)
    
    rowversionstamp = Column(Integer, default=1)    
    
class User(Base, ColumnMixin):
    
    #__bind_key__ = 'appmeta'
    
    __tablename__ = "mt_user"  
    
    id = Column(Integer, Sequence('mt_user_id_seq'), primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    info = Column(Unicode(200) )
    createdon = Column(DateTime)
    active  = Column(Integer, default = 1) 
    rowversionstamp  = Column(Integer, default = 1) 
    
    def __init__(self, username, email, createdon):
        self.username = username
        self.email = email
        self.info = u"码博科技，2013"#.encode('GB2312')
        self.createdon = createdon

    def __repr__(self):
        return '<User %r>' % self.username    

    
class Role(Base, ColumnMixin):
    
    __tablename__ = "mt_role"  
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String(40))
    fullname = Column(String(40))
    password = Column(String(40))
 
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
 
    def __repr__(self):
        return """<User("%s","%s", "%s")>""" % (self.name, self.fullname, self.password)    

class Employee(Base, ColumnMixin):
    
    __tablename__ = "mt_employee"  
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String(40))
    fullname = Column(String(40))
    password = Column(String(40))
 
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
 
    def __repr__(self):
        return """<User("%s","%s", "%s")>""" % (self.name, self.fullname, self.password)        