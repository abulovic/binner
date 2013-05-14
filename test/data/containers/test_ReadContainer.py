import sys, os
sys.path.append(os.getcwd())
import unittest

from data.containers.read import ReadContainer

class ReadContainerTest(unittest.TestCase):

    def setUp(self):
        self.read_cont = ReadContainer()
        self.aln_file = './test/data/containers/.data/example.in'

    def tearUp(self):
        pass

    def testReadCount(self):
        '''
        Tests whether the number of reads in the read container
        is consistent with the number of reads in the 
        alignment file.
        '''
        self.read_cont.populate_from_aln_file(self.aln_file)
        reads_cont = self.read_cont.read_repository.keys()
        reads_file = self._load_read_ids()

        for read_id in reads_file:
            self.assertTrue(read_id in reads_cont, msg = "Read ID %s not in read container." % read_id)
        self.assertEqual(len(reads_cont), 100)

    def testCorrectAlignmentNumber (self):
        '''
        Test the loader for correct number of alignments.
        Test file organized so that read ID specifies number
        of alignments.
        '''
        aln_file = './test/data/containers/.data/aln_num.in'
        self.read_cont.populate_from_aln_file(aln_file)
        for (read_id, read) in self.read_cont.read_repository.items():
            self.assertEqual(int(read_id), len(read.get_alignments()))

    def _load_read_ids (self):
        aln_fhandle = open(self.aln_file, 'r')
        nextline = aln_fhandle.readline
        read_ids = []
        while(True):
            line = nextline()
            if not line: break
            read_id = line.split(',')[0]
            read_ids.append(read_id)
        aln_fhandle.close()
        return read_ids


if __name__ == '__main__':
    unittest.main()