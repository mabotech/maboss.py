
import time

from time import strftime, localtime

def get_time(t1, t2):

    v =  strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    return "%s [%s,%s]" % (v, t1, t2)
    

if __name__ == '__main__':
    
    print get_time('a','b')