
import os
import time

LABEL_BASE = 'C:/MTP/mabotech/maboss1.2/var/printing'

def file_gen(label_base):
    
    label_base = LABEL_BASE
    
    label_today = label_base +os.sep + time.strftime('%Y%m%d')
    
    if not os.path.exists(label_today):
        os.mkdir(label_today)    
    
    info = "zpl here"
    serialno = '89011230'
    fn = 'esn%s.prn' % (serialno)
    
    output = label_today + os.sep + fn
    
    print output
    
    fh = open(output, 'w')
    fh.write(info)
    fh.close()
    
    
    
if __name__ == '__main__':
    
    file_gen("")
    
    
    
    