
from mabolab.database.dbsession import get_db
from ..utils.singleton import Singleton

class Base(object):
    
    __metaclass__ = Singleton
    
    def __init__(self, *args):
        
        self.db =  get_db()
        pass
    