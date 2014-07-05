# -*- coding: utf-8 -*-





import logging
import logging.handlers
import logging.config
"""
if __name__ == "__main__":
    from mabolab.database.config import LOGGING
    logging.config.dictConfig( LOGGING )

log = logging.getLogger(__name__)
"""

#from mabolab.database.dbsession import get_db

import gevent
from gevent import Timeout

import subprocess

#import time
#import gevent

from mabolab.core.base import Base

"""
from flask.config import Config

settings = Config("" )

settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')

#settings['APP_NAME'] = "label_print"
"""

base = Base()


db = base.get_db() 

log = base.get_logger()

settings = base.get_config()


from mabolab.label.str_format import PrnFactory

#from mabolab.common.base import Base
from mabolab.common.singleton import Singleton
#from mabolab.utils.singleton import Singleton

from mabolab.config.configuration import JSONConfiguration

from mabolab.database.utils import row2dict

#from config import DB_URL, DB_ECHO

#from config import LOGGING_CFG_SRV
#logging.config.fileConfig(LOGGING_CFG_SRV)

from certificate_label import CertificateLabel

from certificate_data import CertificateData

#from twisted.internet import reactor

class LabelPrint(Singleton):
    
    """
    - print prn file to workstation printer by lpr
    - query printer status by lpq
    """
    
    #__metaclass__ = Singleton
    
    def __init__(self):
                
        #self.db = get_db()
        
        TEMPLATE_BASE = 'C:/MTP/mabotech/maboss1.2/maboss/repository/label2/templates'
        
        super(LabelPrint, self).__init__()
        
        self.pf = PrnFactory("{abc}")
        
        self.workstation_printer = {}
        
        self.get_config()
        
        self.get_setting()
        
        
    def save_prn(self, label_name, label_str):
        
        base_path = ""
        
        filename = "%s/%s.prn" % (base_path, label_name)
        
        fh = open(filename, 'w')
        fh.write(label_str)
        fh.close()
        
        return filename
        
    def get_config(self):
        
        sql = """select id, workstation, printer_name, ip_address, template_path, spool_address
                    from MT_T_Workstation_Printer where active = 1 """
                    
        rtn = db.session.execute(sql)
        
        rows = rtn.fetchall()

        for row in rows:
            workstation =  row[1]
            self.workstation_printer[workstation] =  row2dict(row)            
            log.debug(self.workstation_printer)
    
    def refresh_config(self):
        
        log.info("update printer config")
        
        self.get_config()
        
        log.info(self.workstation_printer)
        pass
        
    def get_setting(sef):
        
        pass
        

    def query_status(self, workstation):
        """
        
        """
        
        lpq = settings['LPQ']
        
        printer_ip = self.workstation_printer[workstation]['ip_address']        
        printer_name = self.workstation_printer[workstation]['printer_name']   
        
        cmd = '%(lpq)s -S %(printer_ip)s -P %(printer_name)s' % {'lpq':lpq, 'printer_ip':printer_ip, 'printer_name':printer_name}
        
        log.debug( cmd )
        
        try:
            
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            #print p1.pid

            #print p1.returncode 

            output = p1.communicate()[0]
            
            v = output.strip() 

            #print "[%s]" % ( v)
            
            
            if v.count('Error')==0:
                return ('ok',printer_ip)
            else:
                return ('err',printer_ip)
        
        except:
            
            return ('err',printer_ip)
            
            #pass
        
        
    def query_fields(self, workstation):        
        
        sql = "select 1, user"
       
        v = self.db.execute(sql)
        
        log.debug( v.fetchall() )
        
        #self.print_label()
        
        pass
        
    def read_template(self):
        """
        
        """
        pass
        
    def generate_prn(self, data):
        """
        
        """
        temlate = ""
        
        fields = {'abc':'esn000123'}
        
        #print self.pf.get_prn(fields)
        
    def print_label(self, workstation, fields, type = 'a'):
        """
        
        """

        cl = CertificateLabel()
        
        serialno = fields['serialno']        
        model = fields['model']     

        serial_model_dict = settings['SERIAL_MODEL_DICT']        
        
        engine_serial = serial_model_dict[model]  
        
        insp_date =fields['insp_date']
        
        createdby = fields['employee']
        
        printer_ip = self.workstation_printer[workstation]['ip_address']        
        printer_name = self.workstation_printer[workstation]['printer_name']        
        template_path = self.workstation_printer[workstation]['template_path']
        
        (file_name, certificate_no, validation_code) = cl.file_gen(serialno, model, engine_serial, insp_date, workstation, template_path)

        #log.debug(settings)
        
        #gevent.sleep(5)
        
        #text = "abc"        

        #file_name = 'esn%s.prn' % (serialno)
        
        lpr = settings['LPR']

        cmd = '%(lpr)s -S %(printer_ip)s  -P %(printer_name)s %(file_name)s' % {'lpr': lpr, 
                'printer_ip': printer_ip, 
                'printer_name': printer_name, 
                'file_name': file_name }

        log.debug( cmd )
        
        cd = CertificateData()
        
        status = 1
        
        production_license = settings['PRODUCTION_LICENSE']
        
        #move to OK block
        
        #cd.save(serialno, certificate_no, validation_code, model, engine_serial, insp_date, status, createdby)

        
        #timeout = Timeout(5, Exception)
        #timeout.start()
        
        try:

            
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            #print p1.pid

            #print p1.returncode 

            output = p1.communicate()[0]

            v = output.strip() 
            

            
            #v = ""

            #print "[%s]" % ( v)
            
            if v.count('Error'):
                #self.process_error(fn, type)
                #pass
                log.error(v)
                return ('err:%s' %(serialno), certificate_no, validation_code)
            else:
                #self.process_ok(fn, type)
                #pass         
                

                cd.save(serialno, certificate_no, validation_code, model, engine_serial, insp_date, status, production_license, createdby)
                        
                
                return ("ok", certificate_no, validation_code)

        except Exception, e:
            
            #self.process_error(fn, type)          
            
            log.error(e.message)
            
            return  ('err',certificate_no, validation_code)
        
        #finally:
        #    timeout.cancel()

    def process_ok(self,  filename, type):
        """
        
        """
        #print "=="*20
        
        log.debug("good:%s" % ( filename )  )     

        
        if type == 'm':
            #print 'manually'
            pass
        else:
            pass

    def process_error(self, filename, type):
        """
        
        """
        log.debug("error:%s" % ( filename )  )     
        
        if type == 'm':
        
            #print 'manually / error'
            pass

        else:
            pass
            
    
    def printit(self, workstation, fields):
        """
        
        """
        
        #printer_ip = '127.0.0.2'
    
        type = 'm'
        
        return self.print_label(workstation, fields, type)            
        
class P1(LabelPrint):
    
    def __init__(self, workstation):
        
        super(LabelPrint, self).__init__(workstation)
        pass    

class P2(LabelPrint):

    def __init__(self, workstation):
        #super(LabelPrint, self).__init__(workstation)
        pass
        
        
if __name__ == "__main__":

    lp = LabelPrint()
    
    lp.get_config()
