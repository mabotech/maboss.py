# -*- encoding: utf-8 -*-

import sqlalchemy.pool as pool

DBPool = None

def get_params():
    
    db_type = 'oracle'
    ds_string = 'flxuser/flxuser@mesdb'
    
    #db_type = 'mssql'
    #ds_string = 'DSN=fn183;Database=bcflexnet;UID=cimuser;PWD=cimplus'
    
    return (db_type, ds_string)    

def getconn():  
    
    (db_type, ds_string) = get_params()
    
    
    if db_type == 'oracle':
        
        import cx_Oracle
        
        try:
            c = cx_Oracle.connect(ds_string) 
            
        except Exception,e:
            #print e.message
            raise Exception(e.message)
            
    elif db_type == 'mssql':
        
        import pyodbc
        
        pyodbc.pooling=False
        c = pyodbc.connect(ds_string, autocommit=True)
        
    else:
        raise Exception('please check the db_type: %s' %(db_type))      

    return c


def init_pool():
    
    global DBPool
    
    #c = getconn(db_type, ds_string)
    
    DBPool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)
    
    return DBPool




# #########################

def test():    

    conn = DBPool.connect()    
    print id(conn)
    # use it
    cursor = conn.cursor()
    sql = "select count(1) from process"
    
    sql = "select user from dual"
    
    t = cursor.execute(sql)
    
    print t.fetchall()


if __name__ == '__main__':
    
    ds_string = 'DSN=fn183;Database=bcflexnet;UID=cimuser;PWD=cimplus'
    
    ds_string = 'flxuser/flxuser@mesdb'
    
    #'DSN=flexnet;Database=flexnet;UID=flxuser;PWD=flxuser'
    db_type = 'mssql'
    db_type = 'oracle'
    
    init_pool()
    
    for i in range(0,3):
        test()
