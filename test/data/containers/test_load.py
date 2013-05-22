import unittest
import sys, os
sys.path.append(os.getcwd())

from data.containers.load import fill_containers
from ncbi.db.mock_db_access import MockDbQuery

class ContainerLoadingTest (unittest.TestCase):

    def setUp(self):
        pass
    def tearUp(self):
        pass

    def testMockLoading (self):
        '''
        Tests if data population in containers works.
        Only tests if API is consistent, doesn't test if 
        the data inside the containers is consistent.
        '''
        aln_file = './test/solver/read2cds/.test_data/lisa.in'
        cds_fasta = './test/solver/read2cds/.test_data/cds.fa'
        db_access = MockDbQuery(cds_fasta)
        fill_containers(aln_file, db_access)

if __name__ == '__main__':
    unittest.main()