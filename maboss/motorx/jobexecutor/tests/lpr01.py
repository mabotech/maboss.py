
import os

import subprocess



def printing():

    text = "abc"

    printer_ip = '127.0.0.1'

    prn_file = 'a1.txt'

    cmd = 'lpr -S %s  -P TLP2844 %s' %(printer_ip, prn_file)

    print cmd

    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    print p1.pid

    print p1.returncode 

    output = p1.communicate()[0]

    print "[%s]" % ( output.strip() )