
from datetime import datetime

"""
SA row to dict
"""
def row2dict(row):
    
    d = {}
    
    for column in row.keys():
        
        v = getattr(row, column)
        if isinstance(v, datetime):
            v = v.isoformat()
        
        d[column] = v

    return d