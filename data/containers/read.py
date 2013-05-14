from data.read import Read

class ReadContainer (object):
    ''' Contains all the reads loaded from an 
        alignment file. Can be queried by read id.
    '''
    def __init__(self):
        """
        (dict) read_repository Dictionary where value is (Read)read and key is (str)read id.
        """
        self.read_repository = {}
        
    def populate_from_aln_file (self, read_alignment_file):
        ''' Adds all the reads in the alignment file to the
            read repository.
            This is the first stage of filling the read container.
        '''
        aln_file = open(read_alignment_file, 'r')
        for line in aln_file.readlines():
            self._add_read_from_str(line)

    def populate_cdss (self, record_container):
        '''
        Coding sequences are determined for every read alignment.
        @param record_container (RecordContainer)
        '''
        for read in self.fetch_all_reads(format=iter):
            for read_alignment in read.get_alignments(format=iter):
                read_alignment.determine_coding_seqs(record_container)
    
    def fetch_read (self, read_id):
        if self.read_repository.has_key(read_id):
            return self.read_repository[read_id]
        else:
            raise KeyError("Read repository doesn't contain read associated with read ID: {0}".format(read_id))


    def fetch_all_reads (self, format=iter):
        return format(self.read_repository.values())
    
    def _add_read_from_str (self, read_str):
        try:
            read = Read.from_read_str(read_str)
        except IndexError, e:
            print e
            return
        # read identifier must be unique
        assert (not self.read_repository.has_key(read.id))
        self.read_repository[read.id] = read
        
