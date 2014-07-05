import os

import random
import unittest

from mabo.opc.opclib import OPCClient

class TestConfigFunctions(unittest.TestCase):

    def setUp(self):
        
        
        self.opcc = OPCClient()
        
    def test_connect(self):
        
        self.opcc.connect()
        
        
    def test_write(self):
        self.opcc.write()
        
        
    def test_read(self):
        self.opcc.read()
        
    
    
if __name__ == '__main__':
    unittest.main()           
        