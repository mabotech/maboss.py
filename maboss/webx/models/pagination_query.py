# -*- coding: utf-8 -*-

import os

import re

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

from ..models import get_db

db = get_db()


class PaginationQuery(object):
    
    def __init__(self):
        
        #self.session = DBSession()
        
        rowcount = 0
        
        page = 0
        
        current_page = 0
        
        total_page = 0

        rawstr = r"""select (.*) from"""

        self.compile_obj = re.compile(rawstr,  re.IGNORECASE| re.MULTILINE)
        
    
    def pages(self, total, limit):
        
        return  int(ceil(total / float(limit)))
        
        
    def _get_total_rows(self, sql):
        
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
        
        rtn = db.session.execute(sql)
        
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
                data[key].append( (item[key]) )
                
        return data        

    def query(self, i_sql, select_page, limit):

        #sql = "select sysdate from dual"
        
        offset = limit * select_page
        
        total = self._get_total_rows(i_sql)
        
        total_pages = self.pages(total , limit)        

        if db.engine.name == 'oracle': 
            
            sql = """select /*+ First_Rows */ 
            * from (
            select rownum rn, A.*
            from (       
            %s
            ) A where rownum <= %s
            ) B
            where rn     >  %s
            """  % (i_sql,  offset, offset-limit)
            
        elif db.engine.name == 'postgresql': 
            offset = limit * (select_page - 1)
            
            i_sql = re.sub('^\s*select\s+', 'select row_number() over(order by id desc) as rn, ', i_sql, flags=re.IGNORECASE)
            
            log.debug(i_sql)
            
            sql = "%s \n limit %s offset %s" % (i_sql, limit, offset)
            pass
            
        else:
            
            raise Exception("not implemation for this dialect %s ") % (db.engine.name)           
            
        #current_page = select_page
        
        log.debug(sql)
        
        v = db.session.execute(sql)
        
        keys = v.keys()
        #data = v.fetchall()        
        
        data = self._get_array(keys, v.fetchall())
        
        rowcount = v.rowcount
        
        return (total_pages, rowcount, keys, data)