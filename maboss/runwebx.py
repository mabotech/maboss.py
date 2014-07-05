
import os, sys

#import logging
#import logging.handlers
#import logging.config

#from kserver import config  

#logging.config.fileConfig(config.LOGGING)

from config import CENTRAL_CONFIG

if 'threading' in sys.modules:
        #raise Exception('threading module loaded before patching!')
        pass

      
from gevent import monkey
# patch_all
monkey.patch_all()


PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(__file__))
)

FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR, os.pardir)

if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) \
        and not FLASK_JSONRPC_PROJECT_DIR in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)





from flask.config import Config

settings = Config("")

settings.from_pyfile(CENTRAL_CONFIG)

settings['APP_NAME'] = "webx"

from mabolab.core.base import Base

base = Base(settings)
db = base.get_db()
log = base.get_logger()
from webx.apps import create_app
app = create_app( CENTRAL_CONFIG ) 

base.set_app(app)


from gevent.wsgi import WSGIServer

from gevent.pool import Pool







#print dir(log)

#print dir(log.handlers)



jsonrpc = base.get_jsonrpc()

import webx.api.user
import webx.api.article

def run():      
   
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    
    
 
    host = app.config['HOST']
    
    port = app.config['PORT']
    
    debug = app.config['DEBUG']
    
    from webx.addons.mobility.weixin import weixinapi
    app.register_blueprint(weixinapi, url_prefix='/mobi')
    
    import webx.addons.mobility.webapi
    
    #app.host = host 
    #app.port = port
    
    #app.debug = True
    log.debug("\n"+"=="*40 + "\n"+"=="*12+"  MaboTech WebX starting...  "+ "==" *12)
    log.debug("%s:%s[debug:%s]" %(host, port, debug))
    
    app.run(host = host, port = port, debug = debug)
    
    #log.error(app.url_map)   
    
    #gevent http server:
    
    #pool = Pool(200)
    #http_server = WSGIServer((host, port), app, spawn=pool)
    
    #http_server.serve_forever()
    

    
def stop():
    log.debug("\nWebX stopping...")
    #stop_nginx()
    pass
    

if __name__ == "__main__":
    
    run()
    
    