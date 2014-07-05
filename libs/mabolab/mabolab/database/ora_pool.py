

from sqlalchemy import create_engine

from litex.cxpool import CxOracleSessionPool


def get_user():
    
    return "flxuser"

pool = CxOracleSessionPool(
    'oracle://flxuser:flxuser@mesdb/flxnet',
    min_sessions=1,
    max_sessions=5,
    increment=1,
    user_source=get_user
    )
    
    
engine = create_engine('oracle://flxuser:flxuser@mesdb/flxnet', pool=pool)

conn = engine.connect()

res = conn.execute('select user from dual')

res.fetchone()