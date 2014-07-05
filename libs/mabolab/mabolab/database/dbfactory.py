# -*- coding: utf-8 -*-

from .dbsession import DBSession

"""
MariaDB?

MongoDB?

Redis?

Memcached?

Riak?

"""

class OracleSession(DBSession):
    
    def __init__(self, db_url, echo):
        
        super(OracleSession, self).__init__(db_url, echo)
        pass
        
    def get_db_type(self):
        return "oracle"
    
    
class PGSession(DBSession):
    
    def __init__(self, db_url, echo):
        
        super(PGSession, self).__init__(db_url, echo)
        pass
        
    def get_db_type(self):
        return "postgresql"        
    
class SQLite(DBSession):
    def __init__(self, db_url, echo):
        
        super(SQLite, self).__init__(db_url, echo)
        pass

class MySQL(DBSession):
    def __init__(self, db_url, echo):
        
        super(MySQL, self).__init__(db_url, echo)
        pass
        
    
class MSSQL(DBSession):
    def __init__(self, db_url, echo):
        
        super(MSSQL, self).__init__(db_url, echo)
        pass

class ODBC(DBSession):
    
     def __init__(self, db_url, echo):
        
        super(ODBC, self).__init__(db_url, echo)
        pass   
    
    
def get_db(db_type, settings):
    """
    factory
    * settings
    """
    
    if db_type == 'oracle':
        
        db_url = settings['ORA_URL']
        
        echo = settings['DB_ECHO']
        
        db = OracleSession(db_url, echo)
        
    elif db_type == 'postgresql':
        
        db_url = settings['PG_URL']
        
        echo = settings['DB_ECHO']
        
        db = PGSession(db_url, echo)
        
    else:
        
        raise Exception("wrong db type:%s" %(db_type) )
    
    return db