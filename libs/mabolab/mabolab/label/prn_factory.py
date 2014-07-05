# -*- coding: utf-8 -*-

import re

"""
parse zpl, epl file, replace placeholder with real label content

"""

class PrnFactory(object):
    
    """
    prn file factory, generate real prn file by parse prn template which placeholders like  {Placeholder} 
    
    """
    def __init__(self, prn_str):
        
        """
        
        """
        
        self.lines = [] 
        
        self.tpl = prn_str.split('\n')
        
        self._parse()
    
    def _parse(self):  
        
        """
        split line by {|}
        """
        
        for line in self.tpl:
            
            list = re.split('{|}', line)
      
            self.lines.append(list)

        
    def gen_prn(self, labels):
        
        """
        
        """
        
        out = ''
        
        for line in self.lines:
            
            for item in line:
                if item in labels:
                    out = out + "%s"%(labels[item])  #.encode('utf8')
                else:
                    out = out + "%s"%(item)
            out = out + "\n"
                    
        return out                

if __name__ == "__main__":

    prn_str1 = """  abc {xyz}     
        def {xyz}     
        -- {abc} ; """ 
        
    fh = open('template1.prn', 'r')
    
    prn_str = fh.read()
    
    prnf = PrnFactory(prn_str)
    
    labels = {'xyz':3223, 'abc':'sn00001'}
    
    y = prnf.gen_prn(labels)
    
    print y    
    
    labels = {'xyz':123, 'abc':'sn00566'}
    
    y = prnf.gen_prn(labels)
    
    print y
    
    v = re.split('col\d*_', 'col_username') 
    
    print v[-1]