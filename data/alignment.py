from data.containers.record import RecordContainer
from utils.location import Location

class ReadAlnLocation (object):
    """ Contains information on alignment location on 
        an NT nucleotide string
    """
    
    record_container                = RecordContainer.Instance()
    def __init__ (self, read_id, nucleotide_accession, db_source, genome_index, score, 
                  location_span, complement, active=True):
        self.read_id                = read_id
        self.nucleotide_accession   = nucleotide_accession
        self.db_source              = db_source
        self.genome_index           = genome_index
        self.score                  = score
        self.location_span          = location_span
        self.complement             = complement
        self.active                 = active
        self.determine_coding_seqs()
    
    def set_active (self, active):
        '''
        Sets active status for the read alignment.
        Inactive reads do not go into CDS alignments.
        '''
        self.active = active

    def set_potential_host_status (self, potential_host):
        '''
        Set to true if organism is potential host [child of 
        animalia kingdom]
        @param potential_host (boolean) 
        '''
        self.potential_host = potential_host

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
        if (other == None): return False
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

    def is_active(self):
        '''
        Checks whether CDS alignment is active. 
        If all the CDSAlnSublocations are inactive, then the whole CdsAlignment
        is inactive.
        '''
        for cds_aln_subloc in self.aligned_regions.values():
            if cds_aln_subloc.active:
                return True
        return False

    def get_active_alignment_cnt (self):
        '''
        Counts the number of CdsAlnSublocations which
        have been marked as active
        @return (int) number of active alignments
        '''
        active_sublocations = 0
        for cds_aln_subloc in self.aligned_regions.values():
            if cds_aln_subloc.active:
                active_sublocations += 1
        return active_sublocations

    def get_key (self):
        pass
        
    def contains_read (self, read_id):
        ''' Determines whether this CDS alignment contains 
            a subalignment mapped to the specified read.
        '''
        return True if self.aligned_regions.has_key(read_id) else False
        
    def __str__(self):
        tab = " " * 2
        ret = "CdsAlignment\n"
        ret += tab + "cds: " + str(self.cds) + "\n"
        ret += tab + "aligned_regions:\n"
        for (key, aln_reg) in self.aligned_regions.items():
            ret += tab*2 + "(key) " + key + ":\n"
            ret += tab*3 + str(aln_reg).replace("\n", "\n"+(tab*3)) + "\n"
        return ret

    
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

    def __str__(self):
        tab = " "*2
        ret = "CdsAlnSublocation\n"
        ret += tab + "read_id:  " + str(self.read_id) + "\n"
        ret += tab + "location: " + str(self.location) + "\n"
        ret += tab + "score:    " + str(self.score) + "\n"
        ret += tab + "active:   " + str(self.active)
        return ret

