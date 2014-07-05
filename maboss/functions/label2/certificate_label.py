# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
import logging.config


#import profile
import time
from time import strftime, localtime
from datetime import datetime



from sqlalchemy import String, Integer
from sqlalchemy.sql.expression import text , bindparam, outparam

from mabolab.common.singleton import Singleton
from mabolab.core.base import Base

from idgen import idgen1

if __name__ == '__main__':
    from flask.config import Config
    settings = Config("" )
    settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')
    settings['APP_NAME'] = "certificate_label"
    base = Base( settings)
    db = base.get_db("oracle") 

else:   
    base = Base()
    db = base.get_db("oracle") 
    settings = base.get_config()
    

log = base.get_logger()
    


class CertificateLabel(Singleton):
    """
    
    """
    def __init__(self):
        
        super(CertificateLabel, self).__init__()
        
        self.template_str = {}
        
        
    def _get_verification_code(self, serialno, insp_date):
        
        salt = "%s%s" % (serialno, insp_date)
        
        return idgen1(salt)
        
    def _get_certificate_no(self):
        """ call stored procedure """
        
        sql = """MT_SP_GETNEXTCERTNO2 (:I_FACILITY, :O_CertNo, :O_Message )"""

        #bind parameters and set out parameters
        params =  [
            bindparam('I_FACILITY', 'GCIC'),
            outparam('O_CertNo', String), 
            outparam('O_Message', String)
            ]  
        
        #call stored procedure
        rtn = db.call_sp(sql, params)
         
        return rtn['O_CertNo']
        
    def _get_template(self, workstation, template):
        
        if workstation not in self.template_str:
            
            label_base = settings['TEMPLATE_BASE']
            
            full_path = os.sep.join([ label_base, template])
            
            if not os.path.exists(full_path):
                raise Exception("template[%s] not found" % (full_path) )
            
            else:
                # load new template
                t = time.time()
                with open(full_path, 'rb') as fh:
                
                    template_str = fh.read()
                    
                    self.template_str[workstation] = template_str

                #fh.close()
                    
        return self.template_str[workstation]
        
        
    def _get_prn(self, template, fields):
        
        #print template
        #print fields
        
        s = template.format(**fields)
        
        return s.replace('\n','')
        
        
    def file_gen(self, serialno, model, engine_serial, insp_date, workstation, template):
        
        label_base = settings['LABEL_BASE']
        
        #serial_model_dict = settings['SERIAL_MODEL_DICT']
        
        label_today = label_base +os.sep + time.strftime('%Y%m%d')
        
        if not os.path.exists(label_today):
            os.mkdir(label_today)    
        
        
        prn_template = self._get_template(workstation, template)
        
        sql = """select certificate_no from mt_t_certificate where serialno = '%s' """ %(serialno)
        log.debug("=="*20)
        log.debug(sql)
        rtn = db.session.execute(sql)
        
        row = rtn.fetchone()
        
        if rtn.rowcount == 1:
            certno = row[0]
            log.debug("CertificateNo exists")
        else:        
            certno = self._get_certificate_no()
        
        qrcode = self._get_verification_code(serialno, insp_date)
        
        #engine_serial = serial_model_dict[model]
        
        license = settings['PRODUCTION_LICENSE']
        
        fields = {'ESN':serialno, 'Model':model, 'Serial':engine_serial, 'InspDate' : insp_date, 
                    'License':license, 'CertNo':certno, 'QR_Code':qrcode}
        
        prn_str = self._get_prn(prn_template, fields)

        fn = 'esn%s.prn' % (serialno)
        
        output = label_today + os.sep + fn    
        t = time.time()
        with open(output, 'w') as fh:
            fh.write(prn_str)
        return (output, certno, qrcode)
    
    
    
def test():

    cl =  CertificateLabel()

    print cl.file_gen('89002220', '65900', 'cert04.prn')

    
if __name__ == "__main__":    
    test()