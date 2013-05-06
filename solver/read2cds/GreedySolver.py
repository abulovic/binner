from Read2CDSSolver import Read2CDSSolver

class GreedySolver (Read2CDSSolver):
    """ Implementation of Read2CDSSolver that uses greedy algorithm to decide to which CDS does read belong.
    CDS with best coverage is taken and all its active reads are and removed(deactivated) from other CDSs. 
    Coverage of other CDSs is then updated. Process is repeated until there are no more unprocessed active reads left.
    """

    def __init__(self):
        super(GreedySolver, self).__init__()
        # Dictionary where key is CdsAlignment, value is coverage.
        # Already calculated coverages are remembered here.
        self._coverages = {}

        
    def map_reads_2_cdss(self, cds_aln_container):
        super(GreedySolver, self).map_reads_2_cdss(cds_aln_container)
        # Dictionary of cds alignments from cds alignment container
        cds_alns = self._cds_aln_container.cds_repository 

        # Create set that contains read_id for each active read.
        # Read is active if there is active aligned region for that read (there may be more then one). 
        active_reads = set()
        for cds_aln in cds_alns.values():
            for aln_reg in cds_aln.aligned_regions.values():
                if self._is_read_active(aln_reg):
                    active_reads.add(aln_reg.read_id)
        # Number of unprocessed active reads.                    
        num_unproc_active_reads = len(active_reads)
        
        # Dictionary that contains entryes from cds alignment container which have been processed.
        processed_cds_alns = {}
        
        # Until there are no unprocessed active reads left, do following:
        #     Find cds alignment with highest coverage among unprocessed alignments,
        #     move it to processed alignments (its reads are also considered processed then)
        #     and all deactivate in other unprocessed cds algns all active reads from this cds algn.
        while (num_unproc_active_reads > 0):
            best_cds_aln_coverage, best_cds_aln_key = None, None # Cds alignment with highest coverage.
            # Iterate through cds alignments and find the cds alignment with highest coverage.
            for (key, cds_aln) in cds_alns.items():
                cds_aln_coverage = self._get_coverage(cds_aln)
                if best_cds_aln_key == None or cds_aln_coverage > best_cds_aln_coverage:
                    best_cds_aln_coverage = cds_aln_coverage
                    best_cds_aln_key = key
            best_cds_aln = cds_alns[best_cds_aln_key]
        
            # Move best cds to processed cds alignments (and remove it from cds alignment container)
            processed_cds_alns[best_cds_aln_key] = best_cds_aln
            del cds_alns[best_cds_aln_key]

            # For all reads in best cds alignment that are active:
            #    Deactivate them in all other cdss (and update/recalculate coverage for those cdss)
            for aln_reg in best_cds_aln.aligned_regions.values():
                if (self._is_read_active(aln_reg)):
                    num_unproc_active_reads -= 1
                    for cds_aln in self._cds_aln_container.read2cds[aln_reg.read_id]:
                        self._deactivate_read(cds_aln.aligned_regions[aln_reg.read_id])
                        self._coverages.pop(cds_aln, None) # removes coverage which forces recalculation

        # Move proccesed cds alignments back to cds alignment container
        cds_alns.update(processed_cds_alns)

        
    def remap_reads_from_cds(self, cds_aln):
        super(GreedySolver, self).remap_reads_from_cds(cds_aln)
        raise Exception ("Not yet implemented!")

    
    def _get_coverage(self, cds_aln):
        """ If coverage was already calculated before then it is just returned.
        Otherwise coverage is calculated, stored for later and then returned.
        @param (CdsAlignment) cds_aln
        @return (float) coverage
        """
        # If coverage was not calculated before, calculate it and remember it for later.
        if not (cds_aln in self._coverages):
            self._coverages[cds_aln] = self._calc_coverage(cds_aln)

        return self._coverages[cds_aln]
            

    def _calc_coverage(self, cds_aln):
        """ Calculates coverage of given cds alignment.
        Coverage is calculated as sum of lengths of aligned regions divided by number of aligned regions.
        @param (CdsAlignment) cds_aln
        @return (float) coverage
        """
        # Aligned region is part of a read that intersects with cds.
        coverage = 0
        for aln_reg in cds_aln.aligned_regions.values(): # aln_reg is of type CdsAlnSublocation
            location = aln_reg.location # location is of type Location
            coverage += location.length()
        coverage = coverage / float(len(cds_aln.aligned_regions))
        return coverage
            
            
