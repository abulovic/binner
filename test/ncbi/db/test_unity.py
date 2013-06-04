# -*- coding: utf-8 -*-
'''
Created on Jun 4, 2013

@author: marin
'''
import unittest
from ncbi.db.unity import UnityCDS

class Test(unittest.TestCase):


    def testUnityCDSCreation(self):
        data = {        
            'id': 1,
            'db': 'gb',
            'version' : 'A00001.1',
            'nucl_gi' : 2,
            'taxon' : 3,
            'location' : 'complement(1..10)',
            'protein_id' : 'pid',
            'locus_tag' : 'locus2',
            'product' : 'product1',
            'gene' : 'gene3',
            'prot_gi' : 4,
            'cds': None
        }
        
        cds = UnityCDS(data)
        self.assertEqual(1, cds.id, 'id should be 1')
        self.assertEqual('gb', cds.db, 'db should be gb')
        self.assertEqual('A00001.1', cds.version, 'version should be A00001.1')
        self.assertEqual(2, cds.nucl_gi, 'nucl_gi should be 2')
        self.assertEqual(3, cds.taxon, 'taxon should be 3')
        self.assertEqual('complement(1..10)', cds.location, 
                         'location should be complement(1..10)')
        self.assertEqual('pid', cds.protein_id, 'protein_id should be pid')
        self.assertEqual('locus2', cds.locus_tag, 'locus_tag should be locus2')
        self.assertEqual('product1', cds.product, 'product should be product1')
        self.assertEqual('gene3', cds.gene, 'gene should be gene2')
        self.assertEqual(4, cds.prot_gi, 'prot_gi should be 4')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUnityCDSCreation']
    unittest.main()