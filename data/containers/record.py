
class RecordContainer (object):
    ''' 
    Serves as a local Record Repository.
    If a GenBank/EMBL/DDBJ record has already been 
    fetched from the database, it can be fetched localy
    from this record repository. Records are stored in a dictionary
    where key is their nucleotide accession (NCBI), and value 
    is object of type :class:`ncbi.db.genbank.Record` or :class:`ncbi.db.embl.Record`
    It has to have a database access. Correct way to use RecordContainer is::

        db_access = DbQuery()
        record_cont = RecordContainer()
        record_cont.set_db_access(db_access)
        record_cont.populate(read_container)
    '''

    def __init__ (self):
        self.record_repository  = {}
        self.num_missing_records = 0
    
    def get_num_missing_records_stats(self):
        missed_recs = self.num_missing_records 
        all_recs = len(self.record_repository)
        return {'num_missing_records':missed_recs,
                'num_all_records':all_recs,
                'missing_records_percentage':
                '{0:.2f}'.format(missed_recs/float(all_recs)*100)+'%'}

    def set_db_access(self, db_query):
        '''
        Sets database access for RecordContainer

        :param db_query: database access object :class:`ncbi.db.access.DbQuery`
        '''
        assert (hasattr(db_query, 'get_record'))
        self.db_query = db_query

    def populate (self, read_container):
        '''
        Populates the record container with all the records 
        that have produced significant alignments.

        :param read_container: Instance of :class:`data.containers.read.ReadContainer` 
            which has gone through the first stage of populating.
        '''
        reads = read_container.fetch_all_reads(format=iter)
        for read in reads:
            for read_alignment in read.get_alignments(format=iter):
                self.fetch_record(read_alignment.nucleotide_accession)

    def fetch_record (self, nucleotide_accession):
        '''
        Fetch record by nucleotide accession.
        :param nucleotide_accession: string which corresponds to NCBI nucleotide accession
        :rtype: :class:`ncbi.db.genbank.Record` or :class:`ncbi.db.embl.Record`
        '''
        self._add_record(nucleotide_accession)
        return self.record_repository[nucleotide_accession]

    def fetch_all_records (self, format=iter):
        '''
        Fetches all loaded records in a specified format.
        :param format: all default python collection formats including iterator
        :rtype: format(list of tuples (nucleotide_acession, Record))
        '''
        assert (format in [iter, list, set])
        return format(self.record_repository.items())
        
    def _add_record (self, nucleotide_accession):
        ''' 
        Adds the record from database if not already present.
	    If unable to find entry in database, stores None instead.

        :param nucleotide_accession: string which corresponds to NCBI nucleotide accession
        '''
        try:
            getattr(self, 'db_query')
        except AttributeError:
            raise AttributeError("RecordContainer has not attribute 'db_query'. Did you forget to envoke set_db_access()?")
        name = record_id.split('.')[0]
        if not self.record_repository.has_key(record_id):
            record = self.db_query.get_record(name)
            try :
                getattr(record, 'name')
                self.record_repository[record_id] = record
            except AttributeError:
                log.info("No record with ID %s", str(record_id))
                self.record_repository[record_id] = None
                self.num_missing_records += 1
