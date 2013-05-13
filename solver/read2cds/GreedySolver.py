# @author: Martin Sosic, sosic.martin@gmail.com
from Read2CDSSolver import Read2CDSSolver
from utils.location import Location

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
        """ @overrides
        """
        super(GreedySolver, self).map_reads_2_cdss(cds_aln_container)
        # Dictionary of cds alignments from cds alignment container (key is cds)
        cds_alns = self._cds_aln_container.cds_repository 

        # Create set that contains read_id for each active read.
        # Read is active if there is active aligned region for that read (there may be more then one). 
        active_reads = set()
        for cds_aln in cds_alns.values():
            for aln_reg in cds_aln.aligned_regions.values():
                if aln_reg.active:
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
                if aln_reg.active:
                    num_unproc_active_reads -= 1
                    for cds_aln in self._cds_aln_container.read2cds[aln_reg.read_id]:
                        if not(cds_aln is best_cds_aln):
                            cds_aln.aligned_regions[aln_reg.read_id].active = False
                            self._coverages.pop(cds_aln, None) # removes coverage which forces recalculation
                            
        # Move proccesed cds alignments back to cds alignment container
        cds_alns.update(processed_cds_alns)

        
    def remove_cds_and_remap_reads(self, cds_aln):
        """ @overrides 
        Each read is remaped to alternative cds alignment with highest coverage.
        Coverage for modified cds alignments is then recalculated.
        Given cds alignment is deleted from container.
        """
        super(GreedySolver, self).remove_cds_and_remap_reads(cds_aln)
        # Dictionary where key is read_id and value is cds alignment to which it maps.
        # If it does not map to any cds alignment then value is None.
        new_read_mappings = {}

        for aln_reg in cds_aln.aligned_regions.values():
            if aln_reg.active:
                # Find alternative cds alignment with highest coverage
                best_alt_cds_aln = None
                for alt_cds_aln in self._cds_aln_container.read2cds[aln_reg.read_id]:
                    if best_alt_cds_aln == None or self._get_coverage(alt_cds_aln) > self._get_coverage(best_alt_cds_aln): 
                        best_alt_cds_aln = alt_cds_aln
                # Activate it in best alternative cds alignment (if there is one)
                if (best_alt_cds_aln != None):
                    best_alt_cds_aln.aligned_regions[aln_reg.read_id].active = True
                # Add mapping to output dictionary
                new_read_mappings[aln_reg.read_id] = best_alt_cds_aln

        # Delete original cds alignment
        del self._cds_aln_container.cds_repository[cds_aln.cds]
        # Remove original cds alignment from read2cds
        for cds_alns in self._cds_aln_container.read2cds.values():
            if cds_aln in cds_alns: cds_alns.remove(cds_aln)

        # Force recalculation of coverage for updated cds alignments by forgeting coverage
        for updated_cds_aln in set(filter(lambda x: x != None, new_read_mappings.values())):
            del self._coverages[updated_cds_aln]

        return new_read_mappings

    
    def _get_coverage(self, cds_aln):
        """ If coverage was already calculated before then it is just returned.
        Otherwise coverage is calculated, stored for later and then returned.
        @param (CdsAlignment) cds_aln
        @return (float) coverage
        """
        if not (cds_aln in self._coverages):
            self._coverages[cds_aln] = self._calc_coverage(cds_aln)
        return self._coverages[cds_aln]            

    def _calc_coverage(self, cds_aln):
        """ Calculates coverage of given cds alignment.
        Coverage is calculated as sum of lengths of aligned regions divided by length of cds.
        @param (CdsAlignment) cds_aln
        @return (float) coverage
        """
        # Aligned region is part of a read that intersects with cds.
        coverage = 0
        for aln_reg in cds_aln.aligned_regions.values(): # aln_reg is of type CdsAlnSublocation
            location = aln_reg.location # location is of type Location
            coverage += location.length()
        coverage = coverage / float(Location.from_location_str(cds_aln.cds.location).length())
        return coverage
            
            
