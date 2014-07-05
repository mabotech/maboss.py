# -*- coding: utf-8 -*-

import sys

import re

#sys.path.append('c:/MTP/apps/database')

#from .error import InvalidUsage

from mabolab.core.base import Base

base = Base()
db = base.get_db() #'postgresql'  #default db is Oracle
log = base.get_logger()

settings = base.get_config()



from datetime import datetime
import time

from flask import Flask, Blueprint, current_app, jsonify, request

import random

from mabolab.database.pagination_query import PaginationQuery

#from ...models.models import User

#from ...common.dynamic_query import get_conditions

certificate =  Blueprint('certificate', __name__)

#@query.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response        


def get_conditions(request, query_col, table_alias,  db_type):
    
    
    log.debug(request.form )
    
    query_str = request.form.get('search','')
    
    page =  request.form.get('page', 1, type=int) 
    limit = request.form.get('limit', 15, type=int)
    
    date_from = request.form.get('date_from', '')
    date_to = request.form.get('date_to','')
    
    sort_by =   request.form.get('sort_by','')
    sort_order =  request.form.get('sort_order','ASC')
    
    where = []
    
    if query_str != '':        
        where.append("%s like '%%%s%%'"  % (query_col, query_str) )       
    
    
    if db_type == 'oracle':
        if date_from != '':
             where.append( "%s.lastupdateon >= to_date('%s:00:00:00','YYYY-MM-DD HH24:MI:SS')" %(table_alias, date_from) )
        if date_to != '':
            where.append( "%s.lastupdateon <= to_date('%s 23:59:59', 'YYYY-MM-DD HH24:MI:SS')" %(table_alias, date_to))
    else:
        if date_from != '':
             where.append( "%s.lastupdateon >= '%s 00:00:00'" %(table_alias, date_from) )
        if date_to != '':
            where.append( "%s.lastupdateon <= '%s 23:59:59'" %(table_alias, date_to) )       

    if len(where)>0:
        where_clause = ' and '.join(where)
    else:
        where_clause = None
    
    orderby = " order by 1 asc" #certv.lastupdateon desc  # TODO : remove hardcode,  order by 1 desc / order by default column index
    
    log.debug(sort_by)
    
    if sort_by != '':
        #split and get the column name
        colname = sort_by.replace("_",".",1) # re.split('_', sort_by) 
        orderby = " order by %s %s" % (colname, sort_order)
        
    return (page, limit, where_clause, orderby)

@certificate.route("/" , methods=['GET', 'POST'])
def index():
    
    #db.create_all()
    
    #raise InvalidUsage('This view is gone', status_code=410)
    
    log.debug(request.form)
    
    """ 
    log.debug("--"*20)
    log.debug(request.environ)
    log.debug(request.query_string)
    log.debug(current_app.config)
    """
    db_type = db.get_db_type()
    
    table_alias = "certv"
    query_col = "certv.serialno"
    (page, limit, where_clause, orderby) = get_conditions(request, query_col, table_alias, db_type)
    
    t = int(time.time() %100 )

    #dd = dir(db.session)
    
    
    #dd = dir(db.session.bind)#("appmeta")
    
    v = random.randint(65, 91)

    x = chr(v)
    
    #admin = User('admin_%s_%s' % (x , t) , 'admin_%s_%s@example.com' % (x, t) ,  datetime.now() )

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
    
    try:
        workstations = settings['WORKSTATIONS']
        
        workstations_str = ','.join(map(lambda s:"'%s'" % (s), workstations))
        
        serialno_prefix = settings['SERIALNO_PREFIX']
        
        day_offset = settings['DAY_OFFSET']
        
        log.debug(where_clause)
        
        if where_clause == None:
            
            sql = """SELECT sn.serialno as serialno, sn.workstation as workstation, 
    DP.DP_MOD_NAME as model, 
    nvl(cert.status,0) as printed,
    cert.certificate_no as certificate_no,
    cert.createdon as printedon, sn.lastupdateon as lastupdateon
    FROM cob_t_serial_no sn
    inner join cob_t_serial_no_dataplate sd on sd.serial_no = sn.serialno
    inner join cob_t_dataplate dp on DP.DP_BUILD_DATE = SD.BUILD_DATE and DP.DP_SO_NO = SD.SHOP_ORDER_NO
    left join MT_T_CERTIFICATE cert on sn.serialno = cert.serialno
    WHERE  sn.serialno LIKE '%(serialno_prefix)s%%' 
    and sn.status=3 and sn.createdon>sysdate-%(day_offset)s and sn.workstation in (%(workstations_str)s)
    """  %{'serialno_prefix':serialno_prefix, 'workstations_str':workstations_str, 'day_offset':day_offset}
        
            sql = """SELECT certv.serialno, certv.workstation, certv.model, certv.printed, 
            certv.certificate_no, certv.printedon, certv.lastupdateon
    FROM mt_v_certificate certv
    WHERE  certv.serialno LIKE '%(serialno_prefix)s%%' 
    and certv.status=3 and certv.lastupdateon>sysdate-%(day_offset)s and certv.workstation in (%(workstations_str)s)
    """  %{'serialno_prefix':serialno_prefix, 'workstations_str':workstations_str, 'day_offset':day_offset}
    
        else:
            sql = """SELECT sn.serialno as serialno, sn.workstation as workstation, 
    DP.DP_MOD_NAME as model, 
    nvl(cert.status,0) as printed,
    cert.certificate_no as certificate_no,
    cert.createdon as printedon,sn.lastupdateon as lastupdateon
    FROM cob_t_serial_no sn 
    inner join cob_t_serial_no_dataplate sd on sd.serial_no = sn.serialno
    inner join cob_t_dataplate dp on DP.DP_BUILD_DATE = SD.BUILD_DATE and DP.DP_SO_NO = SD.SHOP_ORDER_NO 
    left join MT_T_CERTIFICATE cert on sn.serialno = cert.serialno
    WHERE  %(where_clause)s and sn.serialno LIKE '%(serialno_prefix)s%%' 
    and sn.status=3 and sn.createdon>sysdate-%(day_offset)s and sn.workstation in (%(workstations_str)s)
    """ % {'where_clause': where_clause, 'serialno_prefix':serialno_prefix, 
                    'workstations_str':workstations_str, 'day_offset':day_offset}
                    
                    
            sql = """SELECT certv.serialno, certv.workstation, certv.model, certv.printed, 
            certv.certificate_no, certv.printedon, certv.lastupdateon
    FROM mt_v_certificate certv
    WHERE  %(where_clause)s and certv.serialno LIKE '%(serialno_prefix)s%%' 
    and certv.status=3 and certv.lastupdateon >sysdate-%(day_offset)s 
    and certv.workstation in (%(workstations_str)s)
    """ % {'where_clause': where_clause, 'serialno_prefix':serialno_prefix, 
                    'workstations_str':workstations_str, 'day_offset':day_offset}                    
    
    except Exception, e:
        
        log.error(e.message)
        
    sql = sql + orderby
    
    log.debug(sql)
        
    #users = db.session.execute(sql)
    
    pq = PaginationQuery(db)

    (total_pages, rowcount, keys, data) = pq.query(sql, page, limit, orderby)
    
    #data = db.get_data(keys, data)
    
    return  "%s" %  ( jsonify(result = data, total_pages = total_pages,  rowcount = rowcount, time = time.time()).data  )
    
@certificate.route("/user")
def new_user():
    info =  request.args['info']
    
    user = User('abc2', 'email2@mabo.com', datetime.now() )
    
    user.info = info
    
    db.session.add(user)
    
    db.session.commit()
    
    return info

@certificate.route("/print")
def print_label():
    
    t = time.time()
    if 'esn' in request.args:
        esn = request.args['esn']
    else:
        esn = ""
    
    t2 = time.time()-t
    
    return "%s,%s" % ("json", jsonify(t = t2, b = [1,2,3, esn]).data )


@certificate.route("/printer_config")
def json():
    
    t = time.time()
    
    return "%s,%s" % ("json3", jsonify(b = [1,2,3, t]).data )
    