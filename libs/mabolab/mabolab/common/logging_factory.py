
import logging
import logging.handlers
import logging.config


def get_logger(app, LOG_ROOT, LOGGING):
    
    
    #print LOGGING
    
    #LOG_ROOT = ''#'c:/mtp/mabotech/logs/'
    
    LOGGING['handlers']['debug']['filename'] = LOG_ROOT + '%s_debug.log' %(app)
    LOGGING['handlers']['info']['filename'] = LOG_ROOT + '%s_info.log' %(app)
    LOGGING['handlers']['warning']['filename'] = LOG_ROOT + '%s_warning.log' %(app)
    LOGGING['handlers']['error']['filename'] = LOG_ROOT + '%s_error.log' %(app)
    LOGGING['handlers']['performance']['filename'] = LOG_ROOT + '%s_performance.log' %(app)
    
    logging.config.dictConfig( LOGGING )

    log = logging.getLogger(app)
    
    return log
    
    
#

def test(app):
  
    log = get_logger('performance','','')
    
    print app
    
    
    
    log.debug(app+':debug log')
    log.warning(app+':warning log')
    log.error(app+':error log')
    log.info(app+':info log')
    
    
    
if __name__ == '__main__':
    
    test('app2')
    
    test('app1')
    
    test('app2')
    
    
    