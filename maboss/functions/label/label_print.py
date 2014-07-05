# -*- coding: utf-8 -*-

import logging
import logging.handlers
import logging.config

if __name__ == "__main__":
    from mabolab.database.config import LOGGING
    logging.config.dictConfig( LOGGING )

log = logging.getLogger(__name__)


#from mabolab.database.dbsession import get_db

import subprocess

#import time
#import gevent



from mabolab.label.str_format import PrnFactory

from mabolab.common.base import Base
#from mabolab.utils.singleton import Singleton

from mabolab.config.configuration import JSONConfiguration

#from config import DB_URL, DB_ECHO

#from config import LOGGING_CFG_SRV
#logging.config.fileConfig(LOGGING_CFG_SRV)


#from twisted.internet import reactor


        

class LabelPrint(Base):
    
    """
    - print prn file to workstation printer by lpr
    - query printer status by lpq
    """
    
    #__metaclass__ = Singleton
    
    def __init__(self):
                
        #self.db = get_db()
        
        super(LabelPrint, self).__init__()
        
        self.pf = PrnFactory("{abc}")

        self.get_setting()
        
    def save_prn(self, label_name, label_str):
        
        base_path = ""
        
        filename = "%s/%s.prn" % (base_path, label_name)
        
        fh = open(filename, 'w')
        fh.write(label_str)
        fh.close()
        
        return filename
        
    def get_setting(sef):
        
        pass
        

    def query_status(self, printer_ip):
        """
        
        """
        cmd = 'lpq -S 127.0.0.1 -P %s' % (printer_ip)
        log.debug( cmd )
        try:
            
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            #print p1.pid

            #print p1.returncode 

            output = p1.communicate()[0]
            
            v = output.strip() 

            #print "[%s]" % ( v)
            
            
            if v.count('Error'):
                return 'ok'
        
        except:
            
            return 'err'
            
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
        
    def print_label(self, fn, printer_ip, type = 'a'):
        """
        
        """
        
        #gevent.sleep(5)
        
        text = "abc"        

        prn_file = 'a1.txt'

        cmd = 'lpr -S %s  -P TLP2844 %s' %(printer_ip, prn_file)

        log.debug( cmd )
        
        try:

            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            #print p1.pid

            #print p1.returncode 

            output = p1.communicate()[0]
            
            v = output.strip() 

            #print "[%s]" % ( v)
            
            
            if v.count('Error'):
                self.process_error(fn, type)
                #pass
                return 'err'
            else:
                self.process_ok(fn, type)
                #pass         
                return 'ok'

        except Exception, e:
            
            self.process_error(fn, type)          
            
            return 'err'
            

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
            
    
    def printit(self, workstation):
        """
        
        """
        printer_ip = '127.0.0.2'
    
        type = 'a'
        
        return self.print_label("esn0001", printer_ip, type)            
        
class P1(LabelPrint):
    
    def __init__(self, workstation):
        
        super(LabelPrint, self).__init__(workstation)
        pass    

class P2(LabelPrint):

    def __init__(self, workstation):
        #super(LabelPrint, self).__init__(workstation)
        pass
