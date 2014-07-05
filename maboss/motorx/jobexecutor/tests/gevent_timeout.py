

import gevent
from gevent import Timeout

seconds = 1

timeout = Timeout(seconds)
timeout.start()

def wait():
    gevent.sleep(2)

try:
    gevent.spawn(wait).join()
except Timeout:
    print 'Could not complete'