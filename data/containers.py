from data.read		        import Read
from ncbi.genbank.access    import DbQuery
from utils.singleton        import Singleton

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


@Singleton
class CdsAlnContainer (object):
    ''' CDS Alignment Repository serves as the storage for all 
        CDSs reported in the read alignments. 
        CDS alignment is mapped using record id and cds location 
        and can be fetched using the tuple containing 
        (record_id, location)
    '''

    def __init__(self):
        self.cds_repository = {}
        self.record_repository = RecordContainer.Instance()

    
    def populate (self, readCont):

        # Iterate through reads
        num = 0;
        for read in readCont.read_repository.values():

            # Iterate through read alignments
            for readAln in read.alignment_locations:
                num += 1;

                # Ask each alignment to get its colliding cdss - get array of (CDS, Location) tuples


                # Iterate over CDSs
                    
                    # Create / update CDSalignment in container



        print "pogledao sam alignova: %d " % num


    
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

@Singleton
class RecordContainer (object):
    ''' Serves as a local Record Repository.
        If a GenBank/EMBL/DDBJ record has already been 
        fetched from the database, it can be fetched localy
        from the record repository.
    '''
    def __init__ (self):
        self.record_repository  = {}
        
    def set_db_access(self, db_query):
        self.db_query = db_query

    def fetch_record (self, record_id):
        self._add_record(record_id)
        return self.record_repository[record_id]
        
    def _add_record (self, record_id):
        ''' Adds the record from database if not already present
	   If unable to find entry in database, stores None instead.
        '''
	
        if not self.record_repository.has_key(record_id):
	    record = self.db_query.get_record(record_id)
	    try :
		getattr(record, 'name')
		self.record_repository[record_id] = record
	    except AttributeError:
		print "No record with ID {0}".format(record_id)
		self.record_repository[record_id] = None

def fill_containers (alignment_file):

    # enable database access
    dbQuery = DbQuery()
    # create containers
    recordCont = RecordContainer.Instance()
    recordCont.set_db_access(dbQuery)
    readCont   = ReadContainer.Instance()
    cdsAlnCont = CdsAlnContainer.Instance()

    # --------------------------- Populate readCont ---------------------------------- #

    # Populate from the read container
    readCont.populate_from_aln_file(alignment_file)

    # Debugging output
    print "readCont populated!"
    print ( "len(readCont): %d" % len(readCont.read_repository) )

    firstRead       = readCont.read_repository.itervalues().next();
    firstReadAln    = firstRead.alignment_locations[0];

    print "Broj CDSova je: %d" % len(firstReadAln.aligned_cdss)

    # --------------------------- Populate cdsAlnCont ---------------------------------- #

    # Populate cdsAlnCont using readCont
    cdsAlnCont.populate(readCont);

    return (readCont, recordCont, cdsAlnCont)


