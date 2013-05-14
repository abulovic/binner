
class RecordContainer (object):
    ''' Serves as a local Record Repository.
        If a GenBank/EMBL/DDBJ record has already been 
        fetched from the database, it can be fetched localy
        from the record repository.
    '''
    
    def __init__ (self):
        self.record_repository  = {}
        
    def set_db_access(self, db_query):
        '''
        @param: db_query (DbQuery, MockDbQuery)
        '''
        assert (has_attr(db_query, 'get_record'))
        self.db_query = db_query

    def populate (self, read_container):
        '''
        Populates the record container with all the records 
        that have produced significant alignments
        '''
        reads = read_container.fetch_all_reads(format=iter)
        for read in reads:
            for read_alignment in read.get_alignments(format=iter):
                self.fetch_record(read_alignment.nucleotide_accession)

    def fetch_record (self, nucleotide_accession):
        '''
        @param nucleotide_accession (str)
        @return Record (ncbi/db/[genbank/embl])
        '''
        self._add_record(nucleotide_accession)
        return self.record_repository[nucleotide_accession]
        
    def _add_record (self, record_id):
        ''' Adds the record from database if not already present
	   If unable to find entry in database, stores None instead.
        '''
        name = record_id.split('.')[0]
        if not self.record_repository.has_key(record_id):
            record = self.db_query.get_record(name)
            try :
                getattr(record, 'name')
                self.record_repository[record_id] = record
            except AttributeError:
                print "No record with ID {0}".format(record_id)
                self.record_repository[record_id] = None
