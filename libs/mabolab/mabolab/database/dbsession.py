# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import QueuePool

from sqlalchemy import String, Integer
from sqlalchemy.sql.expression import text , bindparam, outparam

from sqlalchemy.ext.declarative import declarative_base

import logging
import logging.handlers
import logging.config

log = logging.getLogger(__name__)

from flask import current_app

from ..utils.singleton import Singleton

from .config import DB_URL, DB_ECHO

Base = declarative_base()


class DBSession(object):
    
    __metaclass__ = Singleton

    def __init__(self, db_url, echo=True):
    
        #db_url =  DB_URL #'oracle+cx_oracle://flxuser:flxuser@localhost:1521/mesdb?charset=utf8'
        
        log.debug(db_url)
        
        #log.debug(current_app.config)
        #db_url = 'postgresql+psycopg2://postgres:py03thon@localhost:5432/maboss'

        #echo = DB_ECHO # False #
        
        #poolclass = QueuePool, 
        # encoding='utf8', convert_unicode=True,    
        self.engine = create_engine(db_url, encoding='utf8', convert_unicode=True,  
                                                echo=echo, echo_pool = True, pool_size=10, max_overflow=0)

        self.session =   sessionmaker(bind=self.engine)()
        

        if  self.engine.name == 'oracle': 
            
            #deal with Chinese
            os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'
            
            #os.environ['TNS_ADMIN'] =
            """
            sql = "alter session set nls_language='ENGLISH'"
            
            print sql
            
            self.session.execute(sql)
            
            self.session.commit()
            """

        #print dir(self.session)
        
    def create_all(self):
        
        Base.metadata.create_all(self.engine)
        
    def get_pool_status(self):
        
        return self.engine.pool.status()

    #oracle
    def call_sp(self, sql, params):         
        
        sql  = """begin %s ; end;""" %(sql)
        t = text(sql, bindparams = params)                
        result = self.session.execute(t)
        
        #self.session.commit()
        
        return result.out_parameters        
        
    def execute(self, sql):   
        
        try:
            rtn = self.session.execute(sql)
            self.session.commit()
            return rtn
        except Exception:
            self.session.rollback()
            raise
        
    def fetchone(self):
        return self.session.fetchone()
        
    def fetchall(self):
        return self.session.fecthall()
        
    def commit(self):
        return self.session.commit()       
        
    #
    def _get_data(self, keys, rows):

        #rowcount = rowproxy.rowcount
    
        #keys = rowproxy.keys() 
        
        data = {}
        
        for key in keys:
            
            data[key] = []            
     
        for item in rows:
            #log.debug(type(item))           
            
            for key in keys:
                #log.debug(key)
                data[key].append( (item[key]) )
                
        return data
      
def init_db():

    pass

#db = DBSession()

def get_db(db_url = None, echo = True):
    
    if db_url == None:

        db_url = DB_URL
        echo = DB_ECHO
    
    db = DBSession(db_url, echo)
    
    #log.debug(">>"*20)
    
    #log.debug(dir(db.engine))
    
    return db
    
def make_dicts(cursor, row):
    return dict((cur.description[idx][0], value)
                for idx, value in enumerate(row))
                
#db.row_factory = make_dicts

                
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv    
    
