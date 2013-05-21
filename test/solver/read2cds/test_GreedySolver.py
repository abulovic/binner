import sys, os
sys.path.append(os.getcwd())
import unittest

from ncbi.db.mock_db_access         import MockDbQuery

from data.containers.read           import ReadContainer
from data.containers.record         import RecordContainer
from data.containers.cdsaln         import CdsAlnContainer

from solver.read2cds.GreedySolver   import GreedySolver
from solver.read2cds.Read2CDSSolver import Read2CDSSolver


class GreedySolverTest (unittest.TestCase):

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
        self.record_cont.populate(self.read_cont)
        self.read_cont.populate_cdss(self.record_cont)
#       Initialize and fill up cds aln container
        self.cds_aln_cont = CdsAlnContainer()
        self.cds_aln_cont.populate(self.read_cont)

        self.greedy_solver = GreedySolver()
        self.greedy_solver.map_reads_2_cdss(self.cds_aln_cont)


    # Ovo sam zakomentirao jer mi nije htjelo raditi onaj drugi test, to je zbog singletona u setUp
    def testAlignmentsCorrectlyInactivated(self):
        '''
        Loads correct results from results file and checks whether 
        all the reads for a CDS listed in the file are active and
        whether all the other reads are inactive.
        '''
        cds2read = self._load_active_reads()

        for (cds, cds_aln) in self.cds_aln_cont.cds_repository.items():
            accession = cds.record_id
            mapped_reads = cds2read[accession]
            for cds_aln_subloc in cds_aln.aligned_regions.values():
                if cds_aln_subloc.active:
                    assert (cds_aln_subloc.read_id in mapped_reads)
                else:
                    assert (cds_aln_subloc.read_id not in mapped_reads)

    def testCdsAlignmentContainerConsistency(self):
        assert(Read2CDSSolver.test_cds_alignment_container_consistency(self.cds_aln_cont) == True)

    def _load_active_reads (self):
        results_fhandle = open(self.results_fpath)
        lines = iter(results_fhandle.readlines())
        cds2read_map = {}
        while (True):
            cds_id = next(lines, None)
            read_ids = next(lines, None)
            if not cds_id: break
            cds2read_map[cds_id.strip()] = read_ids.strip().split(';')
        results_fhandle.close()
        return cds2read_map





if __name__ == '__main__':

    unittest.main()
