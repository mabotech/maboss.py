
from time import time, strftime, localtime, mktime

def weekly(days):
    
    days = [1,2,3,4,5,6,7]
    
    print days
    
    pass


def daily(next):
    
    #run_on = "17:01:02"
    
    x = next.split(":")
    
    if len(x) != 3:
        raise Exception("time format is wrong")
    
    y = map(lambda x : int(x),  x)    
    
    print y
    
    if y[0]>24 or y[0] < 0:
        raise Exception("hour format is wrong")
    
    if y[1]>60 or y[1] < 0:
        raise Exception("minute format is wrong")
    
    if y[2]>60 or y[2] < 0:
        raise Exception("second format is wrong")
        
    now = localtime()

    h23 = mktime([now[0], now[1], now[2], y[0],y[1],y[2],0,0,0])

    hnow = mktime(localtime())

    dur =  h23 - hnow  
    if dur < 0:
        dur = dur + 86400

    print dur
    


def hour():
    
    pass

def minute():
    
    now = localtime()

    #h23 = mktime([now[0], now[1], now[2], 10,28,0,0,288,0])
    """
    0:year
    1:month
    2:day
    
    3:hour
    4:minute
    5:second
    
    """
    if now[4]<59:
        h23 = mktime([now[0], now[1], now[2], now[3],now[4]+1,0,0,0,0])
    else:
        h23 = mktime([now[0], now[1], now[2], now[3]+1,0,0,0,0,0])

    hnow = mktime(localtime())

    dur =  h23 - hnow  
    if dur < 0:
        dur = dur + 86400
        
    print dur
    print h23
        
        
if __name__ == "__main__":

        next = "18:57:40"
        #daily(next)
        
        weekly([])
        