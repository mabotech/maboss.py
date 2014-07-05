# -*- coding: utf-8 -*-

import os

import random
import unittest

from mabo.utils.config import Config

class TestConfigFunctions(unittest.TestCase):

    def setUp(self):
        pass
        
        

        
    def test_basename(self):
        config_file = "mabo.ini"
        self.cfg = Config(config_file)  
        
    def test_fullname(self):
        
        ppath = (os.path.dirname(os.path.abspath(__file__)))
        
        config_file = os.sep.join([ppath, 'mabo.ini'])        

        self.cfg = Config(config_file)  
        
    def test_getOption(self):
        
        config_file = "mabo.ini"
        self.cfg = Config(config_file)        
        self.assertEqual( self.cfg.getOption('main','app_name'),  'xt')
        

    def test_getSections(self):

        config_file = "mabo.ini"
        self.cfg = Config(config_file)
        
        self.assertEqual( self.cfg.sections(), ['main','logging'])

if __name__ == '__main__':
    unittest.main()        