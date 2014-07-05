# -*- coding: utf-8 -*-

import sys

import re

#sys.path.append('c:/MTP/apps/database')

#from .error import InvalidUsage

from mabolab.core.base import Base

base = Base()
db = base.get_db() #'postgresql'  #default db is Oracle
log = base.get_logger()




from datetime import datetime
import time

from flask import Flask, Blueprint, current_app, jsonify, request

import random

from mabolab.database.pagination_query import PaginationQuery

from ...models.models import User

from ...common.dynamic_query import get_conditions

query =  Blueprint('query', __name__)

#@query.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response        

@query.route("/" , methods=['GET', 'POST'])
def index():
    
    #db.create_all()
    
    #raise InvalidUsage('This view is gone', status_code=410)
    
    """
    log.debug("--"*20)
    log.debug(request.environ)
    log.debug(request.query_string)
    log.debug(current_app.config)
    """
    db_type = db.get_db_type()
    
    (page, limit, where_clause, orderby) = get_conditions(request, db_type)
    
    t = int(time.time() %100 )

    #dd = dir(db.session)
    
    
    #dd = dir(db.session.bind)#("appmeta")
    
    v = random.randint(65, 91)

    x = chr(v)
    
    admin = User('admin_%s_%s' % (x , t) , 'admin_%s_%s@example.com' % (x, t) ,  datetime.now() )

    #guest = User('guest%s' %t , 'guest%s@example.com' %t ,   datetime.now())    
  
    try:

        #db.session.add(admin)

        #db.session.add(guest)        
        
        #db.session.commit()
        
        pass
    
    except Exception, e:
        
        db.session.rollback()        
        log.debug( e )        
        #raise Exception(e)    
    
    
    
    if where_clause == None:
        
        sql = """select id, username, email, info, createdon  from mt_user where active = 1""" 
    
    else:
        sql = """select id, username, email, info, createdon  from mt_user where %s and active = 1""" % (where_clause)
        
    sql = sql + orderby
    
    log.debug(sql)
        
    #users = db.session.execute(sql)
    
    pq = PaginationQuery(db)

    (total_pages, rowcount, keys, data) = pq.query(sql, page, limit, orderby)
    
    #data = db.get_data(keys, data)
    
    return  "%s" %  ( jsonify(data = data, total_pages = total_pages,  rowcount = rowcount, time = time.time()).data  )
    
@query.route("/user")
def new_user():
    info =  request.args['info']
    
    user = User('abc2', 'email2@mabo.com', datetime.now() )
    
    user.info = info
    
    db.session.add(user)
    
    db.session.commit()
    
    return info

@query.route("/reprint")
def reprint():
    
    t = time.time()
    if 'esn' in request.args:
        esn = request.args['esn']
    else:
        esn = ""
    
    t2 = time.time()-t
    
    return "%s,%s" % ("json", jsonify(t = t2, b = [1,2,3, esn]).data )


@query.route("/json")
def json():
    
    t = time.time()
    
    return "%s,%s" % ("json3", jsonify(b = [1,2,3, t]).data )
    