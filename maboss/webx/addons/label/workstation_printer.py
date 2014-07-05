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

ENDPOINT_REQ = settings['ENDPOINT_JOBEXECUTOR_REQ']


from msgpack import packb, unpackb
import gevent
import zerorpc

from datetime import datetime
import time

from flask import Flask, Blueprint, current_app, jsonify, request

import random

from mabolab.database.pagination_query import PaginationQuery

from mabolab.database.utils import row2dict

from maboss.models.label.workstation_printer import WorkstationPrinter

from ...common.dynamic_query import get_conditions

ws_printer =  Blueprint('ws_printer', __name__)

#@ws_printer.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response        

@ws_printer.route("/" , methods=['GET', 'POST'])
def index():
    
    
    sql = """select id, workstation, printer_name, ip_address, 
                    spool_address, template_path, lastupdateon, active
                    from mt_t_workstation_printer where active = 1 order by id desc""" #where active = 1 
    
    rtn = db.session.execute(sql)
    
    rows = rtn.fetchall()
    
    data = []
    
    
    for row in rows:      
        
        d = row2dict(row)
        
        data.append(d)
    
    log.debug(sql)
        
    return  "%s" %  ( jsonify(data = data, time = time.time()).data  )
    
@ws_printer.route("/monitor" , methods=['GET', 'POST'])
def monitor():
    
    workstation =  request.form.get('workstation')
    ip_address =  request.form.get('ip_address')
    
    """
    1 success
    2 warning
    3 danger
    """
    
    #query_printer
    
    log.debug("%s,%s" % (workstation, ip_address) )
    
    client = zerorpc.Client(heartbeat=10) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    name = "label2.query_printer"
    
    #{'workstation' : '65900', 'fields':{'serialno':'89011912','employee':'Admin','model':'mod', 'so_no':'SO10087'}
    
    args = packb({'workstation':workstation})
    
    #msg = 'init'
    
    try:
        rtn =  client.execute(name, args)
        
        v = unpackb(rtn)
        
        msg = v['msg']
        
        printer_ip = v['printer_ip']
        
        if msg == 'ok':
            status = 1
        else:
            status = 0
        #log.debug("=="*20)
        #log.debug( msg )
    
    except zerorpc.exceptions.LostRemote, e:
        msg = "exception:"+e.message
        log.debug(e.message)
        status = 0
    finally:
        client.close() 
    
    return jsonify(workstation = workstation, status = status, printer_ip=printer_ip).data
    
 
def update_config():
    
   
    log.debug("update printer config")
    
    client = zerorpc.Client(heartbeat=10) #heartbeat=None
    
    log.info("client connect: %s" % (ENDPOINT_REQ))
    
    client.connect(ENDPOINT_REQ)     
    
    name = "label2.refresh_printer_config"
    
    #{'workstation' : '65900', 'fields':{'serialno':'89011912','employee':'Admin','model':'mod', 'so_no':'SO10087'}
    
    args = packb({'workstation':''})
    
    #msg = 'init'
    
    try:
        rtn =  client.execute(name, args)
        
        v = unpackb(rtn)
        
        msg = v['msg']
        
        #printer_ip = v['printer_ip']
        
        if msg == 'ok':
            status = 1
        else:
            status = 0
        #log.debug("=="*20)
        #log.debug( msg )
    
    except zerorpc.exceptions.LostRemote, e:
        msg = "exception:"+e.message
        log.debug(e.message)
        status = 0
    finally:
        client.close()     
    
@ws_printer.route("/create" , methods=['GET', 'POST'])
def create():
    
    workstation =  request.form.get('workstation')
    printer_name =  request.form.get('printer_name')
    ip_address =  request.form.get('ip_address')
    spool_address =  request.form.get('spool_address')
    template_path =  request.form.get('template_path')
    operator =  request.form.get('employee')
    
    try:
        
        wsp = WorkstationPrinter(workstation, printer_name, ip_address, spool_address, template_path, operator)
    
        db.session.add(wsp)
    
        db.session.commit()
        
        status = "ok"
        record_id = wsp.id
    except Exception, e:
        db.session.rollback()    
        status =  e.message
        record_id = 0
        
    return jsonify(status = status, id =record_id).data


@ws_printer.route("/update" , methods=['GET', 'POST'])
def update():
    
    record_id = request.form.get('id', type=int)

    
    try:
        
        wsp = db.session.query(WorkstationPrinter).filter_by(id=record_id).first()
        
        wsp.workstation =  request.form.get('workstation')
        wsp.printer_name =  request.form.get('printer_name')
        wsp.ip_address =  request.form.get('ip_address')
        wsp.spool_address =  request.form.get('spool_address')
        wsp.template_path =  request.form.get('template_path')
        
        wsp.lastupdatedby =  request.form.get('employee')        
        wsp.lastupdateon = datetime.now()
        
        wsp.rowversionstamp = wsp.rowversionstamp +1
        
        db.session.add(wsp)
    
        db.session.commit()
        
        status = "ok"
        record_id = wsp.id
        
        update_config()
        
    except Exception, e :
        db.session.rollback()    
        status =  e.message
        record_id = 0
        
    return jsonify(status = status, id = record_id).data

@ws_printer.route("/query" , methods=['GET', 'POST'])
def query():
    
    params = request.get_json()
    
        
    return jsonify(params = params, id = 1).data

@ws_printer.route("/delete" , methods=['GET', 'POST'])
def delete():
    
    record_id = request.form.get('id', type=int)
    
    try:
        
        wsp = db.session.query(WorkstationPrinter).filter_by(id=record_id).first()        
       
        wsp.lastupdatedby =  request.form.get('employee')        
        wsp.lastupdateon = datetime.now()
        wsp.rowversionstamp = wsp.rowversionstamp +1
        wsp.active = 0
        
        db.session.add(wsp)
    
        db.session.commit()
        
        status = "ok"
        record_id = wsp.id
    except:
        db.session.rollback()    
        status =  "error"
        record_id = 0
        
    return jsonify(status = status, id = record_id).data
    