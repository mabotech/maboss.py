
import pkg_resources
import win32serviceutil
#from paste.script.serve import ServeCommand as Server
import os, sys
#import ConfigParser

import win32service
import win32event


from scheduler import main, stop

class OutboundService(win32serviceutil.ServiceFramework):
    """NT Service."""

    #d = DefaultSettings()
    #service_name, service_display_name, service_description, iniFile = d.getDefaults()

    _svc_name_ = 'MaboTech_Outbound_FG'
    
    _svc_display_name_ = 'MaboTech_Outbound_FG'
    _svc_description_ = 'MaboTech_Outbound_FG'

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
        
        main()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def SvcStop(self):
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.stop_event)
        
        stop()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
        
        #sys.exit()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(OutboundService)
