# -*- coding: utf-8 -*-

import random
import unittest

class TestSettingsFunctions(unittest.TestCase):

    def setUp(self):
        
        from maboplat.utils.settings import Settings
        
        config_file = "mabo.ini"
        self.settings = Settings(config_file)

    def test_item(self):

        self.assertEqual(self.settings['main.app_name'], 'xt')
         
    #def test_none(self):

    #     self.assertRaises(Exception, self.settings['main.none'])         
         
    def test_getList(self):

        self.assertEqual(self.settings.getList('main.services'), ['JE1', 'JE2', 'JE3'])      
        
    def test_failure(self):
    
        print self.settings['main.failure']        

    def test_long2(self):
    
        print self.settings['main.long2']
         
    def test_long(self):
        
        long = '''select * from employee
where id < {0}
and 1 = 1'''

        longstr = self.settings['main.long']
        
        
        
        self.assertEqual(longstr.format('10'), long.format(10))
         
    def vtest_all(self):

        self.assertEqual(self.settings, {'main.app_name':'xt', 'main.version':'0.1',
            'logging.debug': 'debug.log', 'main.services': 'JE1 , JE2 , JE3',})         

    def test_json(self):
        
        v = self.settings.getJson('main.services_json')

        for item in v:
            print v[item]
        pass


if __name__ == '__main__':
    unittest.main()