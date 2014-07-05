
#from mabolab.common.base import Base
from mabolab.common.singleton import Singleton

class FieldQuery(Singleton):
    """
    inherit Base as a singleton
    """
    def __init__(self):
        
        super(FieldQuery, self).__init__()
        
        
    def  query(workstation):
        
        sql = "select serialno from cob_t_serial_no where status = 3 and not exist ()"
        
        log.debug(sql)
        