from data.read import Read
from ncbidb.access import DbQuery

# TIP: Implement all containers as singletons

class ReadContainer (object):
    ''' Contains all the reads loaded from an 
        alignment file. Can be queried by read id.
    '''
    _instance = None
    def __new__ (cls):
        if not cls._instance:
            cls._instance = super (ReadContainer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.read_repository = {}
        
    def populate_from_aln_file (self, read_alignment_file):
        ''' Adds all the reads in the alignment file to the
            read repository
        '''
        aln_file = open(read_alignment_file, 'r')
        for line in aln_file.readlines():
            self._add_read_from_str(line)
        pass
    
    def fetch_read (self, read_id):
        if self.read_repository.has_key(read_id):
            return self.read_repository[read_id]
        else:
            raise KeyError("Read repository doesn't contain read associated with read ID: {0}".format(read_id))
    
    def _add_read_from_str (self, read_str):
        read = Read.from_read_str(read_str)
        # read identifier must be unique
        assert (not self.read_repository.has_key(read.id))
        self.read_repository[read.id] = read
        
    def add_read (self, read):
        pass


class CdsAlnContainer (object):
    ''' CDS Alignment Repository serves as the storage for all 
        CDSs reported in the read alignments. 
        CDS alignment is mapped using record id and cds location 
        and can be fetched using the tuple containing 
        (record_id, location)
    '''

    _instance = None
    def __new__ (cls):
        if not cls._instance:
            cls._instance = super (CdsAlnContainer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.cds_repository = {}
        self.record_repository = RecordRepository()

        
    def add_cds_alns (self, cds_alignment):
        cds = cds_alignment.cds
        self.cds_repository[(cds.record_id, cds.location)] = cds_alignment
        
    def update_cdss (self, read_id, aln_location, cds_list):
        ''' For all CDSs listed, alignment sublocation is calculated 
            and cds alignment is appropriately updated.
        '''
        for cds in cds_list:
            if not self.cds_repository.has_key(self.get_key(cds)):
                # create new cds alignment
                pass
            else:
                # update cds alignment
                pass
    
    def fetch_cds_alns (self, record_id, location_tuple, complement=False):
        ''' Finds the already reported CDS alignments for the specified location
        '''
        pass
    
    def get_key(self, cds):
        return (cds.record_id, cds.location)


class RecordContainer (object):
    ''' Serves as a local Record Repository.
        If a GenBank/EMBL/DDBJ record has already been 
        fetched from the database, it can be fetched localy
        from the record repository.
    '''

    _instance = None
    def __new__ (cls, db_query):
        if not cls._instance:
            cls._instance = super (RecordContainer, cls).__new__(cls, db_query)
        return cls._instance

    def __init__ (self, db_query):
        self.record_repository  = {}
        self.db_query = db_query
        
    def fetch_record (self, record_id):
        self._add_record(record_id)
        return self.record_repository[record_id]
        
    def _add_record (self, record_id):
        ''' Adds the record from database if not already present
        '''
        pass


def fill_containers (alignment_file):

    # enable database access
    dbQuery = DbQuery()
    # create containers
    recordCont = RecordContainer(dbQuery)
    readCont   = ReadContainer()
    cdsAlnCont = CdsAlnContainer()

    # populate from the read container
    readCont.populate_from_aln_file(alignment_file)

    return (readCont, recordCont, cdsAlnCont)


