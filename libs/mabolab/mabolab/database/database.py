# -*- encoding: utf-8 -*-

"""
SQLAlchemy  support following dialect:

Drizzle | Firebird | Informix | MaxDB | Microsoft Access | Microsoft SQL Server | 
MySQL | Oracle | PostgreSQL | SQLite | Sybase

this Database class support other Database such as Progress

"""

import pprint

#import pyodbc

#pyodbc.pooling=False

from pool import init_pool

#from pool import DBPool

from maboplat.utils.singleton import Singleton

class Database:
    
    """
    database with connection pool
    """
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        """
        init
        """
        
        
        
        DBPool = init_pool()
        
        print "pool:",id(DBPool)
        
        conn = DBPool.connect()  
        
        self.cursor = conn.cursor()
        
        pprint.pprint( dir(self.cursor) )
        
        """
         'arraysize',
         'arrayvar',
         'bindarraysize',
         'bindnames',
         'bindvars',
         'callfunc',
         'callproc',
         'close',
         'connection',
         'description',
         'execute',
         'executemany',
         'executemanyprepared',
         'fetchall',
         'fetchmany',
         'fetchone',
         'fetchraw',
         'fetchvars',
         'inputtypehandler',
         'next',
         'numbersAsStrings',
         'outputtypehandler',
         'parse',
         'prepare',
         'rowcount',
         'rowfactory',
         'setinputsizes',
         'setoutputsize',
         'statement',
         'var'
         """
        
    def callfunc(self):
        pass
        
    def callproc(self):
        pass
        
    def close(self):
        pass
        
    def execute(self, sql):
        return self.cursor.execute(sql)
        
    def fetchall(self):
        rows = self.cursor.fetchall()
        return rows

    def fetchone(self):
        row = self.cursor.fetchone()
        return row
        
if __name__ == '__main__':
    
    for i in range(0, 8):
    
        db = Database()
        
        print id(db)
        
        sql = """
            select mi2.name, mi.name as miname, tt.short, mi.operationid from menu_item mi 
    inner join menu_item mi2 on mi.parentid = mi2.id
    inner join text_translation tt on tt.textid = mi.textid and tt.languageid = 1033
    --left join text_translation tt2 on tt2.textid = mi2.textid and tt2.languageid = 1033
    where
    mi.showmobile = 1  and mi.operationid > 1000
        """
        
        sql = "select user from dual"
        
        db.execute(sql)
        
        rtn = db.fetchall()
        
        for item in rtn:
            print item
        
