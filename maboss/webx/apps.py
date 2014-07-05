# -*- coding: utf-8 -*-

import os, sys



import logging
import logging.handlers
import logging.config

#logging.config.fileConfig('c:/mtp/maboss0.1/configuration/logging.ini')

log = logging.getLogger(__name__)

import json

from flask import Flask, Blueprint, jsonify, request, url_for



from .helpers.register import url, register_rest,register_api
from .helpers.lazy_view import LazyView

"""
from .addons.label.query3 import query
from .addons.label.certificate import certificate
from .addons.label.workstation_printer import ws_printer
from .addons.label.printm import printm
from .addons.scheduler.sch_client import scheduler
from .addons.label import print_man
from .addons.protal import user1
from .addons.protal import user2
"""



#from views.query3 import *
    
def create_app(config_filename):    
    

    app = Flask(__name__)

    #log.debug(config_filename)
    
    app.config.from_pyfile(config_filename)

    #log.debug("main")
    #log.debug("=="*20)
    #log.debug(app)

    #app.debug = True    


    API_BASE = app.config['API']
    
    """
    app.register_blueprint(certificate, url_prefix=API_BASE + '/certificate')

    app.register_blueprint(ws_printer, url_prefix=API_BASE + '/ws_printer')  
    app.register_blueprint(printm, url_prefix=API_BASE + '/printm')  
    
    app.register_blueprint(scheduler, url_prefix=API_BASE + '/sch')  
    """
    
    
    
    #app.add_url_rule('/favicon.ico',
    #             redirect_to=url_for('static', filename='favicon.ico'))

    #app.register_blueprint(query2, url_prefix=API_BASE + '/apps02')       
    
    #app.add_url_rule('/apps/apps30/', view_func=LazyView('maboss.addons.query3.index'), methods=['GET','POST'])
    #url(app, '/apps/apps3/','views.query3.index', methods=['GET','POST'])
    
    #app.add_url_rule('/apps/apps3/reprint', view_func=LazyView('maboss.addons.query3.reprint'), methods=['GET','POST'])
    
    #url(app, '/apps/apps3/reprint', 'views.query3.reprint', methods=['GET','POST'])
    
    #url(app, '/apps/app3/reprint2', 'views.query2.reprint', methods=['GET','POST'])
    
    #register_api(app, user1.UserAPI, 'user_api1', API_BASE +'/apps3/users1/', pk='user_id')
    
    #register_api(app, user2.UserAPI, 'user_api2', API_BASE +'/apps3/users2/', pk='user_id')
    
    #register_rest(app, '/apps/employees/', 'views.employee', pk='uid')
    
    #register_rest(app, '/apps/employees2/', 'views.employee2', pk='uid')
    
    #app.add_url_rule('/apps/apps3/reprint', view_func=LazyBlueprintView('maboss.addons.query3.query', 'query') , methods=['GET','POST'])
    #LazyView('kserver.addons.label.print_man.print_man')
    #app.add_url_rule(API_BASE +'/apps3/print_man', view_func=print_man.print_man , methods=['GET','POST'])
    
    #import api.user
    
    
    
    #log.debug("=="*20)
    log.debug(app.url_map)
    
    #log.debug(url_for("query3.index"))
    
    return app
    
#app.run(host='127.0.0.1', port=6226)

if __name__ == "__main__":
    
    #main()
    pass