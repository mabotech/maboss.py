


LOGGING =  {
    'version': 1,              
    #'disable_existing_loggers': True,
    
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
            
        'performance': {
                'level':'DEBUG',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'performance.log',
                'maxBytes':10240,
                'backupCount':3
            },            
            
        'debug': {
                'level':'DEBUG',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'debug.log',
                'maxBytes':10240,
                'backupCount':3
            },          
            'info': {
                'level':'INFO',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'info.log',
                'maxBytes':10240,
                'backupCount':3
            },   
            'warning': {
                'level':'WARNING',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'warning.log',
                'maxBytes':10240,
                'backupCount':3
            },   
            'error': {
                'level':'ERROR',    
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'error.log',
                'maxBytes':10240,
                'backupCount':3
            }, 
    },
    
    'loggers': {
    
        '': {                  
            'handlers': ['console', 'debug', 'info', 'warning', 'error', 'performance'   ],        
            'level': 'DEBUG',  
            'propagate': True  
        },
        
        'performance': {                  
            'handlers': ['console', 'performance'],        
            'level': 'DEBUG',  
            'propagate': True  
        }        
        
    }
}
