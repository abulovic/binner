from data.containers.record import RecordContainer
from utils.location import Location

class ReadAlnLocation (object):
    """ Contains information on alignment location on 
        an NT nucleotide string
    """
    
    record_container                = RecordContainer.Instance()
    def __init__ (self, read_id, nucleotide_accession, db_source, genome_index, score, 
                  location_span, complement):
        self.read_id                = read_id
        self.nucleotide_accession   = nucleotide_accession
        self.db_source              = db_source
        self.genome_index           = genome_index
        self.score                  = score
        self.location_span          = location_span
        self.complement             = complement
        self.determine_coding_seqs()
    
    @staticmethod
    def parse_location (nucleotide_location_str):
        pass
    
    def getCDSs(self):
        pass

    def determine_coding_seqs (self):
        ''' Determines which of the CDSs in the record aligned_regions
            aligned to the read.
            @return list of tuples (cds, intersecting_location) if such exist, 
            None if record is not available from the database
        '''
        self.aligned_cdss = []
        record = ReadAlnLocation.record_container.fetch_record (self.nucleotide_accession)

        # if not possible to fetch a record from the db, return None
        if not record:
            return None

        for cds in record.cdss:
            cds_location = Location.from_location_str(cds.location)
            location_intersection = cds_location.find_intersection (
                                                                    self.location_span, 
                                                                    self.complement
                                                                    )
            if location_intersection is not None:
                self.aligned_cdss.append ((cds, location_intersection))
        
        return self.aligned_cdss

        
    def set_type (self):
        """ Location can be coding or non-coding
        """
        pass


class CdsAlignment (object):
    ''' Contains all the alignment information for a single
        CDS, meaning: 
        - all the reads mapped to that CDS and
        - their corresponding sublocations
    '''
    
    def __init__ (self, cds):
        self.cds = cds              # CDS object (from Mladen)
        self.aligned_regions = {}   # dictionary of CdsAlnSublocation
        pass
    
    def __hash__ (self):
        return hash ((self.cds.record_id, self.cds.location))

    def __eq__ (self, other):
        return (self.cds.record_id, self.cds.location) == (other.cds.record_id, other.cds.location)

    def add_aligned_sublocation (self, read_id, aligned_location, score):
        ''' Adds an aligned region to the cds unless it comes 
            from the read already present in the aligned regions
            @param read_id read id 
            @param (Location) aligned_location intersection between the CDS and the 
                    alignment location
            @param score alignment score for this read
        '''
        
        # if the CDS has already been covered by the same read in the past,
        # discard this one. 
        if self.aligned_regions.has_key(read_id):
            return
        
        aligned_sublocation             = CdsAlnSublocation (read_id, aligned_location, score)
        self.aligned_regions[read_id]   = aligned_sublocation

    def get_key (self):
        pass
        
    def contains_read (self, read_id):
        ''' Determines whether this CDS alignment contains 
            a subalignment mapped to the specified read.
        '''
        return True if self.aligned_regions.has_key(read_id) else False
        


    
class CdsAlnSublocation (object):
    ''' Represents the sublocation of a CDS covered
        by a single read.
    '''
        
    def __init__ (self, read_id, location, score, active=True):
        ''' @param read_id read ID 
            @param (Location) location intersection location 
            @param score alignment score
            @param (boolean) active If active than it maps to CDS that contains it.
        '''
        self.read_id    = read_id
        self.location   = location
        self.score      = score
        self.active     = active

