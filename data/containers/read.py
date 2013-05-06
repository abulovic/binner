from data.read		    import Read
from utils.singleton    import Singleton

# TIP: Implement all containers as singletons

@Singleton
class ReadContainer (object):
    ''' Contains all the reads loaded from an 
        alignment file. Can be queried by read id.
    '''
    def __init__(self):
        self.read_repository = {}
        
    def populate_from_aln_file (self, read_alignment_file):
        ''' Adds all the reads in the alignment file to the
            read repository
        '''
        aln_file = open(read_alignment_file, 'r')
        for line in aln_file.readlines():
            self._add_read_from_str(line)
    
    def fetch_read (self, read_id):
        if self.read_repository.has_key(read_id):
            return self.read_repository[read_id]
        else:
            raise KeyError("Read repository doesn't contain read associated with read ID: {0}".format(read_id))

    def fetch_all_reads (self):
        return iter(self.read_repository.values())
    
    def _add_read_from_str (self, read_str):
        read = Read.from_read_str(read_str)
        # read identifier must be unique
        assert (not self.read_repository.has_key(read.id))
        self.read_repository[read.id] = read
        
    def add_read (self, read):
        pass
