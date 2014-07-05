# -*- coding: utf-8 -*-

from flask.config import Config

from mabolab.utils.singleton import Singleton

from mabolab.common import logging_factory



class Base(object):
    
    __metaclass__ = Singleton
    
    def __init__(self, settings=None):
        
        self.settings = settings
        
        log_cfg = Config('')

        log_cfg.from_pyfile( settings['LOGGING_CONFIG'])        
        
        self.log = logging_factory.get_logger(settings['APP_NAME'], settings['LOGGING_PATH'], log_cfg['LOGGING'])
        
        self.dbattr_dict = {'ORA':'ora_db','PG':'pg_db', 'DB':'db'}
        
        self.name_dict = {'ORA':'oracle','PG':'postgresql', 'DB':'oracle'}
        
        #import dbsession after logger initialized
        from mabolab.database import dbfactory
        
        for db_type in settings['DB_TYPE']:       

            if not hasattr(self, self.dbattr_dict[db_type]):
                #self.log.debug("set %s" %(db_type) )
                setattr(self, self.dbattr_dict[db_type], dbfactory.get_db(self.name_dict[db_type], settings) )
        
        if not hasattr(self, 'db'):
            setattr(self, 'db', dbfactory.get_db(self.name_dict['DB'], settings) )
        
        #self.log.debug(dir(self))

        
        
        
    def get_config(self):
        
        return self.settings
    
    def get_logger(self):   
        
        return self.log
        
    def get_db(self, db_type=None):
        
        if db_type == None:
            #return self.ora_db
            return self.db
        
        elif db_type == 'oracle':
            return self.ora_db
        
        elif db_type == 'postgresql':
            return self.pg_db
        
        
