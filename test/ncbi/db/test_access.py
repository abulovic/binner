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
        
    def testNcbitaxGi2TaxidQuery (self):
        gi2taxid = self.dbQuery.get_taxids([574262, 574273], format=dict)
        self.assertEqual (gi2taxid, {574262:9606, 574273:9606})
        taxid_list = self.dbQuery.get_taxids ([574262, 574273], format=list)
        self.assertEqual (taxid_list, [9606, 9606])

    def testNcbitaxOrgNameQuery (self):
        org_name = self.dbQuery.get_organism_name(9606)
        self.assertEqual ('Homo sapiens', org_name)
        org_name = self.dbQuery.get_organism_name(-1)
        self.assertEqual((), org_name)

    def testNcbitaxTaxidQuery (self):
        org_name = "Homo sapiens"
        tax_id = self.dbQuery.get_organism_taxid(org_name)
        self.assertEqual(tax_id, 9606)
        tax_id = self.dbQuery.get_organism_taxid('not in database!!!')
        self.assertEqual(tax_id, ())

    def testOrganismRank (self):
        # query by taxid
        rank = self.dbQuery.get_organism_rank(9606, False)
        self.assertEqual(rank, 'species')
        # query by name
        rank = self.dbQuery.get_organism_rank('Homo sapiens', True)
        self.assertEqual(rank, 'species')
        # not in database
        rank = self.dbQuery.get_organism_rank('gargoyle', True)
        self.assertEqual(rank, None)
        
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
