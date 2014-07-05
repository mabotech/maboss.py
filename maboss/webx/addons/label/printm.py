# -*- coding: utf-8 -*-

import sys
import traceback
import re

#sys.path.append('c:/MTP/apps/database')

#from .error import InvalidUsage
from msgpack import packb, unpackb
import gevent
import zerorpc

from mabolab.core.base import Base


base = Base()
db = base.get_db() #'postgresql'  #default db is Oracle
log = base.get_logger()

settings = base.get_config()

ENDPOINT_REQ = settings['ENDPOINT_JOBEXECUTOR_REQ']


from datetime import datetime
import time

from flask import Flask, Blueprint, current_app, jsonify, request

import random

from mabolab.database.pagination_query import PaginationQuery

from mabolab.database.utils import row2dict

from maboss.models.label.certificate_printm import CertificatePrintm

from ...common.dynamic_query import get_conditions

printm =  Blueprint('printem', __name__)


@printm.route("/" , methods=['GET', 'POST'])
def index():
    
    
    sql = """select id, serialno, reason, createdon, createdby from (select id,  serialno, reason, createdon, createdby from mt_t_certificate_printm
                where active = 1  order by id desc) where rownum < 16"""
    
    rtn = db.session.execute(sql)
    
    rows = rtn.fetchall()
    
    data = []
    
    
    for row in rows:      
        
        d = row2dict(row)
        
        data.append(d)
    
    log.debug(sql)
        
    return  "%s" %  ( jsonify(data = data, time = time.time()).data  )

def query_serialno(serialno):
    
    sql = """select DP.DP_MOD_NAME as model,
    TO_CHAR(sn.lastupdateon,'YYYY-MM-DD') as insp_date    
    from cob_t_serial_no sn 
    inner join cob_t_serial_no_dataplate sd on sd.serial_no = sn.serialno
    inner join cob_t_dataplate dp on DP.DP_BUILD_DATE = SD.BUILD_DATE and DP.DP_SO_NO = SD.SHOP_ORDER_NO    
    where sn.serialno = '%s' and sn.status = 3 and sn.active = 1 """ % (serialno)
    
    log.debug(sql)
    
    rtn = db.session.execute(sql)
    
    row = rtn.fetchone()
    log.debug(rtn.rowcount)
    rowcount = rtn.rowcount
    
    if rowcount == 1:
        log.debug("%s,%s,%s" % (rowcount, row[0], row[1]) )
        return (rowcount, row[0], row[1])
    else:
        return (0, 0, 0)
    
def print_label(workstation, serialno, model, insp_date, employee):

    client = zerorpc.Client(heartbeat=3) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    name = "label2.print_label"
    
    #{'workstation' : '65900', 'fields':{'serialno':'89011912','employee':'Admin','model':'mod', 'so_no':'SO10087'}
    
    args = packb({'workstation':workstation, 'fields':{'serialno':serialno,'model':model, 'insp_date':insp_date, 'employee':employee}})
    
    #msg = 'init'
    
    try:
        args =  client.execute(name, args)
        log.debug("=="*20)
        log.debug( unpackb(args) )
    
    except zerorpc.exceptions.LostRemote, e:
        msg = "exception:"+e.message
        log.error(e.message)
        raise Exception("error:"+e.message)
    except Exception, e:
        raise Exception(e.message)
    finally:
        client.close()     
    
    return args
    
@printm.route("/create" , methods=['GET', 'POST'])
def create():
    
    serialno =  request.values.get('serialno')
    
    workstation =  request.values.get('workstation')
    
    reason =  request.values.get('reason')
    
    """
    printer_name =  request.form.get('printer_name')
    ip_address =  request.form.get('ip_address')
    spool_address =  request.form.get('spool_address')
    template_path =  request.form.get('template_path')
    """
    
    employee =  request.values.get('employee')
    
    (v, model, insp_date) = query_serialno(serialno)
    
    engineserial = settings['SERIAL_MODEL_DICT'][model]
    
    if v == 0:
        status = "ESN is wrong"
        log.debug(status)
        return jsonify(status = status, id =v).data
    
    try:
        
        
        args  = print_label(workstation, serialno, model, insp_date, employee)
        
        v = unpackb(args)
        log.debug(v)
        
        msg = v['msg']
        certificate_no = v['certificate_no']
        validation_code = v['validation_code']
        #(certificate_no, validation_code, model, so_no) = ("","","Mod","SO")
        
        if msg.count('err') ==0:
        
            cpm = CertificatePrintm( serialno, certificate_no, validation_code, model, engineserial, insp_date, workstation, reason, 1, employee) #status
            log.debug(cpm)
            db.session.add(cpm)
        
            db.session.commit()
            
            status = "ok"
            record_id = cpm.id
        else:
            
            #raise Exception("printing failed[%s], please check: %s" % (serialno, workstation))
            
            status =  "printing failed[%s], please check: %s" % (serialno, workstation)
            record_id = 0
            
    except Exception, e:
        db.session.rollback()    
        status =  e.message + ":180"
        record_id = 0
        log.error(traceback.format_stack())
        raise(Exception(e.message))
        
    return jsonify(status = status, id =record_id).data


@printm.route("/update" , methods=['GET', 'POST'])
def update():
    
    record_id = request.form.get('id', type=int)

    
    try:
        
        cpm = db.session.query(WorkstationPrinter).filter_by(id=record_id).first()
        
        cpm.workstation =  request.form.get('workstation')
        cpm.printer_name =  request.form.get('printer_name')
        cpm.ip_address =  request.form.get('ip_address')
        cpm.spool_address =  request.form.get('spool_address')
        cpm.template_path =  request.form.get('template_path')
        
        cpm.lastupdatedby =  request.form.get('employee')        
        cpm.lastupdateon = datetime.now()
        
        cpm.rowversionstamp = cpm.rowversionstamp +1
        
        db.session.add(cpm)
    
        db.session.commit()
        
        status = "ok"
        record_id = cpm.id
    except Exception, e :
        db.session.rollback()    
        status =  e.message
        record_id = 0
        
    return jsonify(status = status, id = record_id).data


@printm.route("/delete" , methods=['GET', 'POST'])
def delete():
    
    record_id = request.form.get('id', type=int)
    
    try:
        
        cpm = db.session.query(WorkstationPrinter).filter_by(id=record_id).first()        
       
        cpm.lastupdatedby =  request.form.get('employee')        
        cpm.lastupdateon = datetime.now()
        cpm.rowversionstamp = cpm.rowversionstamp +1
        cpm.active = 0
        
        db.session.add(cpm)
    
        db.session.commit()
        
        status = "ok"
        record_id = cpm.id
    except:
        db.session.rollback()    
        status =  "error"
        record_id = 0
        
    return jsonify(status = status, id = record_id).data
    