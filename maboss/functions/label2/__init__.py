# -*- coding: utf-8 -*-

import sys
"""
if 'threading' in sys.modules:
        raise Exception('threading module loaded before patching!')
        
from gevent import monkey
# patch_all
monkey.patch_all()
"""
import time

import logging
import logging.handlers
import logging.config

log = logging.getLogger(__name__)

from mabolab.core.base import Base
    
if __name__ == "__main__":
    #from mabolab.database.config import LOGGING
    #logging.config.dictConfig( LOGGING )
    from flask.config import Config

    settings = Config("" )

    settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2.2/maboss/configuration/central_config.py')
    
    settings['APP_NAME'] = 'print_label'


    base = Base(settings)
    
    log = base.get_logger()
    
    db = base.get_db("oracle") 
    settings = base.get_config()
    
else:
    
    base = Base()
    
    log = base.get_logger()
    db = base.get_db("oracle") 
    settings = base.get_config()
    
from mabolab.database.utils import row2dict
    
from msgpack import packb, unpackb

from field_query import FieldQuery

from label_print import LabelPrint


def print_label(args):
    
    input = unpackb(args)
    
    workstation = input['workstation']
    
    fields = input['fields']
    
    log.debug("%s:%s" %(workstation, fields))
    
    lp = LabelPrint()
    
    (msg, certificate_no, validation_code) =  lp.printit(workstation, fields)
    
    
    log.debug("%s,%s,%s" %( msg, certificate_no, validation_code) )
    
    return packb({'msg':msg, 'certificate_no':certificate_no,"validation_code":validation_code})
    
    
def print_label_sch(args):
    
    input = unpackb(args)
    
    workstation = input['workstation']
    
    serialno_prefix = settings['SERIALNO_PREFIX']
    
    day_offset = settings['DAY_OFFSET']
    
    sql = """select * from (SELECT sn.serialno as serialno, sn.workstation,
DP.DP_MOD_NAME as model,
TO_CHAR(sn.lastupdateon,'YYYY-MM-DD') as insp_date
FROM cob_t_serial_no sn 
inner join cob_t_serial_no_dataplate sd on sd.serial_no = sn.serialno
inner join cob_t_dataplate dp on DP.DP_BUILD_DATE = SD.BUILD_DATE and DP.DP_SO_NO = SD.SHOP_ORDER_NO
WHERE  
sn.serialno LIKE '%(serialno_prefix)s%%'
and sn.status=3 and sn.createdon>sysdate-%(day_offset)s and workstation in ('%(workstation)s')
and not EXISTS(select 1 from MT_T_CERTIFICATE cert where sn.serialno= cert.serialno)
order by sn.createdon )
where rownum<2
""" % {'serialno_prefix':serialno_prefix, 'workstation':workstation, 'day_offset':day_offset}    
    
    log.debug(sql)
    
    rtn = db.session.execute(sql)
    
    row = rtn.fetchone()
    
    if rtn.rowcount > 0:
        fields = row2dict(row)
        fields['employee'] = 'System'
        
        #fields['license'] = settings['']
        #fields['serial_model'] = settings

    
        log.debug("%s:%s" %(workstation, fields))
        
        lp = LabelPrint()
        
        (msg, certificate_no, validation_code) =  lp.printit(workstation, fields)
        
        
        log.debug("%s,%s,%s" %( msg, certificate_no, validation_code) )
        
        return packb({'msg':msg, 'certificate_no':certificate_no,"validation_code":validation_code})
    else:
        return packb({'msg':'no data', 'certificate_no':'',"validation_code":''})
    
def query_and_print(args):
    
    fq  = FieldQuery()
    
    rows = fq.get_data()
    
    lp = LabelPrint()    
    
    for row in rows:
        
        rtn =  lp.printit(workstation, fields)
    
    return "ok"
    
def refresh_printer_config(args):    
   
    lp = LabelPrint()    
    lp.refresh_config()   
    
    return packb({'msg':'ok'})
    
def query_printer(args):
    
   
    lp = LabelPrint()
    
    input = unpackb(args)
    
    workstation = input['workstation']
    
    (msg, printer_ip) = lp.query_status(workstation)
    
    return packb({'msg':msg, 'printer_ip':printer_ip})
            
            
def test():


    args = packb({'workstation' : '65900', 'fields':{'serialno':'89011912','employee':'Admin','model':'mod', 'so_no':'SO10087'} } )
    
    
    args = packb({'workstation' : '62300'})
    
    #rtn = query_printer(args)
    
    #print rtn
    print_label_sch(args)
    
    
    #print_label(args)
   

    
if __name__ == '__main__':
    
    #import cProfile
    
    #cProfile.run('test()')
    
    test()
    

    #query_printer(args)
    