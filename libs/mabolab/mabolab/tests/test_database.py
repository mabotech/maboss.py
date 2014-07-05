# -*- coding: utf-8 -*-

import random
import unittest

from mabo.database.database import Database

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):        
        
        ds_string = 'DSN=fn183;Database=gf6flexnet_prod;UID=cimuser;PWD=cimplus'        
        db_type = 'mssql'
        
        self.db = Database(ds_string, db_type)        

        
        
    def test_Query(self):
        
        sql = """select top 1 id, createdon from employee   """
        
        self.db.execute(sql)
        
        #rtn = self.db.fetchall()
        row = self.db.fetchone()
        self.assertEqual( row[0], 1)
        #for item in rtn:
        #    print item


if __name__ == '__main__':
    unittest.main()  

