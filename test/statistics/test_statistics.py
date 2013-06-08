import sys, os
sys.path.append(os.getcwd())
import unittest

from ncbi.db.mock_db_access         import MockDbQuery

from data.containers.read           import ReadContainer
from data.containers.record         import RecordContainer
from data.containers.cdsaln         import CdsAlnContainer

from solver.read2cds.BestScoreSolver   import BestScoreSolver
from solver.read2cds.Read2CDSSolver import Read2CDSSolver

from statistics.statistics import *

class StatisticsTest (unittest.TestCase):

    # setUp is executed before each test method
    def setUp(self):
        '''
        @param mock_db_fpath (str) path to syntheticaly created CDSs which serves
        to fill up mock database of records
        @param input_aln_fpath (str) path to input alignment file 
        @param results_fpath (str) path to file with generated correct results 
        greedy solver should generate
        '''        
        self.mock_db_fpath = './test/statistics/.test_data/cds.fa'
        self.input_aln_fpath = './test/statistics/.test_data/lisa.in'
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
        self.cds_aln_cont.populate(self.read_cont.fetch_all_reads())


    def testStatistics(self):
        assert(num_read_alns(self.read_cont) == 22)
        assert(num_active_aligned_regions(self.cds_aln_cont) == 22)
        assert(num_inactive_read_alns(self.read_cont) == 0)
        
        self.bs_solver = BestScoreSolver()
        self.bs_solver.map_reads_2_cdss(self.cds_aln_cont)
        
        records_stats = count_alns_to_record_and_cds(self.read_cont)
        print "Number of records for which we  have stats: %d\n" % len(records_stats)
        for rec_stat in records_stats.values():
            rec_stat.print_data()

        assert(num_active_aligned_regions(self.cds_aln_cont) == 16)
        
        assert(num_cdss(self.cds_aln_cont) == 4)
        assert(num_cdss_with_no_alns(self.cds_aln_cont) == 0)


if __name__ == '__main__':

    unittest.main()
