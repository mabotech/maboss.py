# -*- coding: utf-8 -*-
"""
settings

"""

import simplejson as json


from config import Config

from maboplat.utils.singleton import Singleton


    
def _strip_spaces(alist):
    return map(lambda x: x.strip(), alist)        
        
class Settings(dict):    
    
    """
    subclass of dict 
    settings
    """
    
    __metaclass__ = Singleton

    
    def __init__(self, config_file, ddd=None, **kw):
        
        if ddd is None:
            ddd = {}
            
        dict.__init__(self, ddd, **kw)         
        
        cfg = Config( config_file )
        
        settings = {}
        for section in cfg.sections():
            
            for option in cfg.options(section):
                
                key = ".".join([section, option])
                settings[key] = cfg.getOption(section, option)
        
        self.update(settings)
        
    def getJson(self, key):
        
        jsonstr = self.get(key)

        jsonobj = json.loads( jsonstr )
        
        return jsonobj
        
    def getV(self, sec, key):
        
        return self.get(sec+'.'+key)
        
    def getList(self, key):
        
        val = self.get(key)
        
        if val == None:
            raise Exception('KeyError:%s' % (key))
            
        slist = val.split(',')
        return _strip_spaces(slist)
            
        
    def __getitem__(self, key):
        
        if self.get(key) == None:
            raise Exception('KeyError:%s' % (key))
        
        return self.get(key) #never raises KeyError


def main():    
    """
    main
    """
    from maboplat.static import APP_CONFIG_FILE 
    
    settings = Settings(APP_CONFIG_FILE)
    
    print settings['alert.to']
    
    print settings
    

if __name__ == "__main__":
    main()