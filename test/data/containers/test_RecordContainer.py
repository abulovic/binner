import unittest
import sys,os
sys.path.append(os.getcwd())

from data.containers.record import RecordContainer
from data.containers.read import ReadContainer
from ncbi.db.mock_db_access import MockDbQuery

class RecordContainerTest (unittest.TestCase):

    def setUp(self):
        self.read_container = ReadContainer()
        self.record_container = RecordContainer()

    def tearUp(self):
        pass

    def testFillRecordContainer(self):
        '''Method to test whether record container populating works.
        Uses mock database access to test whether record container
        has correct number of items.'''
        aln_file = './test/solver/read2cds/.test_data/lisa.in'
        cds_fasta = './test/solver/read2cds/.test_data/cds.fa'
        db_access = MockDbQuery(cds_fasta)
        self.record_container.set_db_access(db_access)

        self.read_container.populate_from_aln_file(aln_file)
        self.record_container.populate(
            self.read_container.fetch_all_reads_versions())
        records = self.record_container.fetch_all_records(format=list)
        self.assertEqual (len(db_access.records), len(records))
        
    def testReturnsNoneForNonexistentRecord(self):
        record = self.record_container.fetch_existing_record("XXX")
        self.assertIsNone(record, "No record with version XXX should be found")


if __name__ == '__main__':
    unittest.main()