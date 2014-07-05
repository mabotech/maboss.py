# -*- coding: utf-8 -*-

import sys

#sys.path.append('c:/MTP/apps/database')

#from .error import InvalidUsage

from mabolab.core.base import Base

base = Base()

db = base.get_db()


from mabolab.database.pagination_query import PaginationQuery

from ...models.models import User

from datetime import datetime
import time

from flask import Flask, Blueprint, current_app, jsonify, request

import random

import logging
import logging.handlers
import logging.config

log = logging.getLogger(__name__)

query2 =  Blueprint('query2', __name__)

"""
@query2.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response        
"""

@query2.route("/" , methods=['GET', 'POST'])
def index():
    
    #db.create_all()
    
    #raise InvalidUsage('This view is gone', status_code=410)
    
    """
    log.debug("--"*20)
    log.debug(request.environ)
    log.debug(request.query_string)
    log.debug(current_app.config)
    """
    
    c = request.args.get('callback', '')
    
    log.debug(request.form.get('page', 1, type=int) )
    
    if 'page' in  request.form:
        page =  int(request.form['page'])
    else:
        page = 1
    
    log.debug("=="*20)
    log.debug(page)
    log.debug(request.form )
    log.debug(request.query_string)
    
    if 'limit' in  request.form:
        limit = request.form['limit']
    else:
        limit = 10
    
    """
    index
    
    """
    condition = None
    
    if 'search' in request.form:
        query_str = request.form['search']
        condition = " username like '%%%s%%' and " % (query_str)
    else:
        query_str =None
    
    t = int(time.time() %100 )

    dd = dir(db.session)
    
    
    dd = dir(db.session.bind)#("appmeta")
    
    v = random.randint(65, 91)

    x = chr(v)
    
    admin = User('admin_%s_%s' % (x , t) , 'admin_%s_%s@example.com' % (x, t) ,  datetime.now() )

    #guest = User('guest%s' %t , 'guest%s@example.com' %t ,   datetime.now())
    
    import sys
    log.debug(">>"*20)
    log.debug(sys.stdout.encoding)
    
    try:

        #db.session.add(admin)

        #db.session.add(guest)        
        
        #db.session.commit()
        
        pass
    
    except Exception, e:
        
        db.session.rollback()        
        log.debug( e )        
        #raise Exception(e)    
    
    if query_str == None:
        
        sql = """select id, username, email, info  from mt_user where active = 1  -- order by id desc"""
    
    else:
        sql = """select id, username, email, info  from mt_user where %s active = 1  -- order by id desc""" % (condition)
        
    #users = db.session.execute(sql)
    
    pq = PaginationQuery(db)

    (total_pages, rowcount, keys, data) = pq.query(sql, page, limit)
    
    #data = db.get_data(keys, data)
    
    return  "%s" %  ( jsonify(c=c, data = data, total_pages = total_pages,  rowcount = rowcount, time = time.time()).data  )
    
@query2.route("/user")
def new_user():
    info =  request.args['info']
    
    user = User('abc2', 'email2@mabo.com', datetime.now() )
    
    user.info = info
    
    db.session.add(user)
    
    db.session.commit()
    
    return info

@query2.route("/reprint")
def reprint():
    
    if 'esn' in request.args:
        esn = request.args['esn']
    else:
        esn = ""
    
    t = time.time()
    
    return "%s,%s" % ("json2000", jsonify(b = [1,2,3, esn]).data )


@query2.route("/json")
def json():
    
    t = time.time()
    
    return "%s,%s" % ("json3", jsonify(b = [1,2,3, t]).data )
    