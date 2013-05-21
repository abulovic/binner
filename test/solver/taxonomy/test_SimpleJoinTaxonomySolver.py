import sys,os
sys.path.append(os.getcwd())

import unittest

from solver.taxonomy.SimpleJoinTaxonomySolver import SimpleJoinTaxonomySolver
from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access import DbQuery
from data.containers.load import fill_containers

class SimpleJoinTaxonomySolverTest (unittest.TestCase):
    def setUp(self):
        self.aln_file = 'test/data/containers/.data/empty.in'
        self.tax_tree = TaxTree()
        self.db_access = DbQuery()
        (self.read_cont, self.record_cont, self.cds_aln_cont) = fill_containers(self.aln_file, self.db_access)

    def testRefTaxid (self):
        tax_solver = SimpleJoinTaxonomySolver()
        taxid = tax_solver.get_ref_taxid(502800, self.db_access, self.tax_tree)
        self.assertEqual (taxid, 633)
        taxid = tax_solver.get_ref_taxid(633, self.db_access, self.tax_tree)
        self.assertEqual (taxid, 633)
        

if __name__=='__main__':
    unittest.main()
