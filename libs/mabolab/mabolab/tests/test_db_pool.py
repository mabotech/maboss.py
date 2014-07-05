# -*- coding: utf-8 -*-

import random
import unittest

from mabo.database.pool import init_pool

class TestDBPoolFunctions(unittest.TestCase):

    def setUp(self):       
        
        ds_string = 'DSN=fn183;Database=bcflexnet;UID=cimuser;PWD=cimplus'
        #'DSN=flexnet;Database=flexnet;UID=flxuser;PWD=flxuser'
        db_type = 'mssql'
        
        self.DBPool = init_pool(ds_string, db_type)
        
        
    def test_Query(self):
        
        conn = self.DBPool.connect()   
        cursor = conn.cursor()
        t = cursor.execute("select top 1 10")
        v = t.fetchall()        
        
        self.assertEqual(v[0][0],  10 )




if __name__ == '__main__':
    unittest.main()  
    
    
