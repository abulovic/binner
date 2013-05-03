# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2013

@author: marin
'''
import sys, os
sys.path.append(os.getcwd())

import unittest
from ncbi.db.access import DbQuery 

class Test(unittest.TestCase):


    def setUp(self):
        self.dbQuery = DbQuery(
            genbank_db_url='mysql+mysqldb://root:root@localhost/genbank',
            embl_db_url='mysql+mysqldb://root:root@localhost/embl')


    def tearDown(self):
        pass


    def testGenBankFindReturnsRecord(self):
        record = self.dbQuery.get_record(record_id='AB000181', db_source='gb')
        self.assertIsNotNone(record, "Not found object AB000181 in GenBank")
        
    def testEmblFindReturnsRecord(self):
        record = self.dbQuery.get_record(record_id='AB015437', db_source='embl')
        self.assertIsNotNone(record, "Not found object AB015437 in Embl")

    def testFindNotSupportedTypeThrowsException(self):
        call = lambda x,y: self.dbQuery.get_record(record_id=x, db_source=y)
        self.assertRaises(ValueError, call, x='AB015437', y='xxx')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
