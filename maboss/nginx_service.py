
import os, sys

if 'threading' in sys.modules:
        raise Exception('threading module loaded before patching!')

      
from gevent import monkey
# patch_all
monkey.patch_all()


import pkg_resources
import win32serviceutil
#from paste.script.serve import ServeCommand as Server

import traceback

import win32service
import win32event

import gevent  
import subprocess

from config import NGINX_PATH


def run():
    
    opath = os.getcwd()
    os.chdir(NGINX_PATH)
    cmd = "start nginx -c %s/conf/nginx.conf" %(NGINX_PATH)
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    #log.debug(output)
    os.chdir(opath)
    
def stop():
    cmd = "%s/nginx.exe -s quit" %(NGINX_PATH)
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    #log.debug(output)

class MaboService(win32serviceutil.ServiceFramework):
    """NT Service."""

    #d = DefaultSettings()
    #service_name, service_display_name, service_description, iniFile = d.getDefaults()

    _svc_name_ = "_nginx"
    
    _svc_display_name_ = "_nginx"
    
    _svc_description_ = "nginx web server"

    def __init__(self, args):
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event that SvcDoRun can wait on and SvcStop
        # can set.
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        
        os.chdir(os.path.dirname(__file__))
        
        #s = Server(None)
        #s.run([self.iniFile])
        #jobscheduler.main()
        #win32event.SetEvent(self.start_event)
        
        run()
        
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def SvcStop(self):
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.stop_event)
        
        stop()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
        
        #sys.exit()

if __name__ == '__main__':
    
    try:        
        win32serviceutil.HandleCommandLine(MaboService)        
    except:        
        traceback.print_exc(file=sys.stdout)

