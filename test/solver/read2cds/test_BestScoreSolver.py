import sys, os
sys.path.append(os.getcwd())
import unittest

from ncbi.db.mock_db_access         import MockDbQuery

from data.containers.read           import ReadContainer
from data.containers.record         import RecordContainer
from data.containers.cdsaln         import CdsAlnContainer

from solver.read2cds.BestScoreSolver   import BestScoreSolver
from solver.read2cds.Read2CDSSolver import Read2CDSSolver


class BestScoreSolverTest (unittest.TestCase):

    # setUp is executed before each test method
    def setUp(self):
        '''
        @param mock_db_fpath (str) path to syntheticaly created CDSs which serves
        to fill up mock database of records
        @param input_aln_fpath (str) path to input alignment file 
        @param results_fpath (str) path to file with generated correct results 
        greedy solver should generate
        '''        
        self.mock_db_fpath = './test/solver/read2cds/.test_data/cds.fa'
        self.input_aln_fpath = './test/solver/read2cds/.test_data/lisa.in'
        self.results_fpath = './test/solver/read2cds/.test_data/cds_ordering.txt'
#       Initialize read container
        self.read_cont = ReadContainer()
        self.read_cont.populate_from_aln_file(self.input_aln_fpath)
#       Initialize and fill record container
        self.db_query = MockDbQuery (self.mock_db_fpath)
        self.record_cont = RecordContainer()
        self.record_cont.set_db_access(self.db_query)
        self.record_cont.populate(self.read_cont.fetch_all_reads_versions())
        self.read_cont.populate_cdss(self.record_cont)
#       Initialize and fill up cds aln container
        self.cds_aln_cont = CdsAlnContainer()
        self.cds_aln_cont.populate(self.read_cont)

        self.bs_solver = BestScoreSolver()
        self.bs_solver.map_reads_2_cdss(self.cds_aln_cont)


    def testCdsAlignmentContainerConsistency(self):
        assert(Read2CDSSolver.test_cds_alignment_container_consistency(self.cds_aln_cont) == True)



if __name__ == '__main__':

    unittest.main()
