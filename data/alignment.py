class ReadAlnLocation (object):
    """ Contains information on alignment location on 
        an NT nucleotide string
    """
    
    def __init__ (self, read_id, nucleotide_accession, db_source, genome_index, score, location_span, complement):
        self.read_id                = read_id
        self.nucleotide_accession   = nucleotide_accession
        self.db_source              = db_source
        self.genome_index           = genome_index
        self.score                  = score
        self.location_span          = location_span
        self.complement             = complement
        
        # self.record                 = ReadAlnLocation.fetch_record(nucleotide_accession)
        self.determine_coding_seqs()
    
    @staticmethod
    def parse_location (nucleotide_location_str):
        pass
    
    def getCDSs(self):
        pass

    def determine_coding_seqs (self):
        ''' All the coding sequences should be stored in the 
            CDS alignment repository
        '''
        # self.cdss = self.record.find_cds (self.location_span.to_location_tuple(), 
        #                                  self.complement)
        pass

        
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
        self.aligned_regions = {}
        self.coverage = None
        pass
    
    def add_aligned_sublocation (self, read_id, location, score):
        ''' Adds an aligned region to the cds unless it comes 
            from the read already present in the aligned regions
        '''
        
        if self.aligned_regions.has_key(read_id):
            return
        aligned_location = self.cds.find_intersection(location)
        
        aligned_sublocation             = CdsAlnSublocation (read_id, aligned_location, score)
        self.aligned_regions[read_id]   = aligned_sublocation
        
    def get_coverage (self, update_coverage = False):
        ''' Get the coverage of a CDS calculated based on 
            the aligned regions and quality of the alignments. '''
        if not self.coverage or update_coverage:
            self.coverage = self._recalculate_coverage()
        return self.coverage
    
    def remove_read (self, read_id):
        # _recalculate_coverage
        pass

    def _recalculate_coverage (self):
        ''' Calculate the coverage of a CDS based on 
            the aligned regions and quality of the alignments. '''
        pass

    
class CdsAlnSublocation (object):
    ''' Represents the sublocation of a CDS covered
        by a single read.
    '''
        
    def __init__ (self, read_id, location, score):
        pass

