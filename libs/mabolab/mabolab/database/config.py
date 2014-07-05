# -*- coding: utf-8 -*-

ORA_URL = 'oracle+cx_oracle://flxuser:flxuser@localhost:1521/mesdb?charset=utf8'

PG_URL = 'postgresql+psycopg2://postgres:py03thon@localhost:5432/maboss'

DB_URL = 'oracle+cx_oracle://flxuser:flxuser@localhost:1521/mesdb?charset=utf8'

DB_ECHO = True

LOGGING =  {
    'version': 1,              
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level':'DEBUG',    
            'class':'logging.StreamHandler',
            'formatter':'standard'
        },  
    },
    'loggers': {
        '': {                  
            'handlers': ['console'],        
            'level': 'DEBUG',  
            'propagate': True  
        }
    }
}