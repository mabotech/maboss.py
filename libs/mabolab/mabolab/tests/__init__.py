# -*- coding: utf-8 -*-

import unittest
import doctest


def all_tests_suite():
    
    suite = unittest.TestLoader().loadTestsFromNames([
        #'mabo.tests.test_config',
        #'mabo.tests.test_settings',
        #'mabo.tests.test_wmi',
        #'mabo.tests.test_db_pool',
        #'mabo.tests.test_database',
       ])
    
    return suite


def main():
    
    runner = unittest.TextTestRunner()
    
    suite = all_tests_suite()
    
    raise SystemExit(not runner.run(suite).wasSuccessful())
    


if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()    