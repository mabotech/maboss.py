
import csv


from datetime import datetime

from mabolab.common.singleton import Singleton


class JobInfo(Singleton):
    
    def __init__(self):
        
        self.jobs = {}  #{name : (interval, active, staus, last_run_time), name2:()}
        pass
        
    def get_active(self, name):
        if name in self.jobs:
            return self.jobs[name][1]
        else:
            return 0
        pass

    def set_active(self, name, active):
        if name in self.jobs:
            self.jobs[name][1] = active
            return active
        else:
            return 0
        pass

    def add_job(self, jobid, args):
        #print jobid, args
        if jobid in self.jobs:
            pass
        else:
            self.jobs[jobid] = args
            
    def del_job(self, jobid):
        if jobid in self.jobs:
            del self.jobs[jobid]
        else:
            pass
            
    
    def load(self, fn):
        

        with open(fn, 'rb') as f:
            
            reader = csv.reader(f, delimiter=";", quotechar="\'")
            for row in reader:
                jobid = int(row[0])
                name = row[1].strip()
                
                args = row[2]#.strip()
                
                #args2 = {"ws":62300,"sn":"SN01001"}
                #v = json.dumps(args2)
                #print json.loads(args)
                
                interval = int(row[3])
                
                active = int(row[4])
                now = datetime.now()
                
                self.jobs[jobid] = {'name':name, 'active':active, 'interval':interval, 'args':args, 'last_run_on':None}



if __name__ == "__main__":
    
    jobinfo = JobInfo()
    
    fn = "cron.csv"
    
    jobinfo.load(fn)
    
    print jobinfo.jobs
