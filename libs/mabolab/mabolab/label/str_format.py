# -*- coding: utf-8 -*-

class PrnFactory(object):
    
    """
    
    """
    def __init__(self, template):
        """
        
        """
        self.template = template

    def get_prn(self, fields):
        
        """        
        
        """
        prn = self.template.format(**fields)

        return prn            


if __name__ == "__main__":
    
    template = '''Coordinates: {latitude}, 

    {longitude}'''
    
    fields = {'latitude': '37.24N', 'longitude': '-115.81W'}
    
    pf = PrnFactory(template)
    
    prn = pf.get_prn(fields)
    
    print prn