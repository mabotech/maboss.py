# -*- coding: utf-8 -*-

import os

import re
from datetime import datetime, date
from math import ceil

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




class PaginationQuery(object):
    
    def __init__(self, db):
        
        #self.session = DBSession()
        
        self.db = db
        
        rowcount = 0
        
        page = 0
        
        current_page = 0
        
        total_page = 0

        rawstr = r"""select(.*)from\s+"""

        self.compile_obj = re.compile(rawstr,  re.IGNORECASE| re.MULTILINE |re.DOTALL |re.VERBOSE)
        
    
    def pages(self, total, limit):
        
        return  int(ceil(total / float(limit)))
        
        
    def _get_total_rows(self, sql):
        
        log.debug(sql)
        
        match_obj = self.compile_obj.search(sql)
        
        if match_obj == None:
            raise Exception("can't get total records from sql")
        
        # Retrieve group(s) from match_obj
        all_groups = match_obj.groups()
        
        #print all_groups

        # Retrieve group(s) by index
        group_1 = match_obj.group(1)
        
        #print group_1
        
        sql =  sql.replace(group_1, " count(1) as rcount ")
        
        sql = re.split('\s+order\s+by\s+', sql, flags=re.IGNORECASE)[0]
        
        log.debug(sql)
        
        rtn = self.db.session.execute(sql)
        self.db.session.commit()
        
        #print "=="*20
        #print db.session.get_pool_status()        
        return rtn.fetchone()[0]        
        
    def _get_array(self, keys, rows):

        #rowcount = rowproxy.rowcount
    
        #keys = rowproxy.keys() 
        
        data = {}
        
        for key in keys:
            
            data[key] = []            
     
        for item in rows:
            #log.debug(type(item))           
            
            for key in keys:
                #log.debug(key)
                obj =  item[key]
                if isinstance(obj, datetime) or  isinstance(obj, date)  :
                    """
                    val = '**new Date(%i,%i,%i,%i,%i,%i)' % (obj.year,
                                                      obj.month-1, #here javascript need
                                                      obj.day,
                                                      obj.hour,
                                                      obj.minute,
                                                      obj.second)
                    """
                    data[key].append(obj.isoformat())                                  
                else:
                    data[key].append(obj)
        #log.debug(data)        
        return data        

    def query(self, i_sql, select_page, limit, orderby):

        #sql = "select sysdate from dual"
        
        offset = limit * select_page
        
        total = self._get_total_rows(i_sql)
        
        total_pages = self.pages(total , limit)        

        if self.db.engine.name == 'oracle': 
            
            sql = """select /*+ First_Rows */ 
            * from (
            select rownum rn, A.*
            from (       
            %s
            ) A where rownum <= %s
            ) B
            where rn     >  %s
            """  % (i_sql,  offset, offset-limit)
            
        elif self.db.engine.name == 'postgresql': 
            offset = limit * (select_page - 1)
            
            rownum_clause = 'select row_number() over(%s) as rn, ' %(orderby)
            
            
            i_sql = re.sub('^\s*select\s+',  rownum_clause, 
                i_sql, flags=re.IGNORECASE)
            
            log.debug(i_sql)
            
            sql = "%s \n limit %s offset %s" % (i_sql, limit, offset)
            pass
            
        else:
            
            raise Exception("not implemation for this dialect %s ") % (self.db.engine.name)           
            
        #current_page = select_page
        
        log.debug(sql)
        
        v = self.db.session.execute(sql)
        self.db.session.commit()
        keys = v.keys()
        #data = v.fetchall()        
        
        data = self._get_array(keys, v.fetchall())
        
        rowcount = v.rowcount
        
        return (total_pages, rowcount, keys, data)