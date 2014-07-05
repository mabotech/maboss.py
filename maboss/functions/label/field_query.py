
from mabolab.common.base import Base

class FieldQuery(Base):
    
    def __init__(self):
        
        super(FieldQuery, self).__init__()
        
        
    def  query(workstation):
        
        sql = "select serialno from cob_t_serial_no where status = 3 and not exist ()"
        
        log.debug(sql)
        