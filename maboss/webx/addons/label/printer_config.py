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

from maboss.models.label.printer_config import PrinterConfig

from ...common.dynamic_query import get_conditions

printer_cfg =  Blueprint('printer_cfg', __name__)

def row2dict(row):
    
    d = {}
    
    for column in row.keys():
        
        v = getattr(row, column)
        if isinstance(v, datetime):
            v = v.isoformat()
        
        d[column] = v

    return d

#@printer_cfg.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response        

@printer_cfg.route("/" , methods=['GET', 'POST'])
def index():
    
    
    sql = """select id, workstation, printer_name, ip_address, 
                    spool_address, template_path, lastupdateon
                    from mt_t_printer_config where active = 1 order by id desc"""
    
    rtn = db.session.execute(sql)
    
    rows = rtn.fetchall()
    
    data = []
    
    
    for row in rows:      
        
        d = row2dict(row)
        
        data.append(d)
    
    log.debug(sql)
        
    return  "%s" %  ( jsonify(data = data, time = time.time()).data  )
    
@printer_cfg.route("/create")
def create():
    
    workstation =  request.form.get('workstation')
    printer_name =  request.form.get('printer_name')
    ip_address =  request.form.get('ip_address')
    spool_address =  request.form.get('spool_address')
    template_path =  request.form.get('template_path')
    
    try:
        
        pc = PrinterConfig(workstation, printer_name, ip_address, spool_address, template_path)
    
        db.session.add(pc)
    
        db.session.commit()
        
        status = "ok"
        id = pc.id
    except:
        db.session.rollback()    
        status =  "error"
        id = 0
        
    return jsonify(status = status, id = id).data


@printer_cfg.route("/update")
def update():
    
    t = time.time()
    if 'esn' in request.args:
        esn = request.args['esn']
    else:
        esn = ""
    
    t2 = time.time()-t
    
    return "%s,%s" % ("json", jsonify(t = t2, b = [1,2,3, esn]).data )


@printer_cfg.route("/delete")
def delete():
    
    t = time.time()
    
    return "%s,%s" % ("json3", jsonify(b = [1,2,3, t]).data )
    