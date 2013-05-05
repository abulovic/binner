from Read2CDSSolver import Read2CDSSolver

class GreedySolver (Read2CDSSolver):
    """ Implementation of Read2CDSSolver that uses greedy algorithm to decide to which CDS does read belong.
    CDS with best coverage is taken and all its reads are assigned to it and removed from other CDSs. 
    Coverage of other CDSs is then updated. Process is repeated until there are no more reads left.
    """

    def __init__(self):
        # Dictionary where key is cds, value is coverage. Already calculated coverages are remebered here.
        self._coverages = {} 

    def map_reads_2_cdss(self):
        super(GreedySolver, self).map_reads_2_cdss();

        best_cds_aln = None # Cds alignment with highest coverage.
        # Iterate through cds alignments and find the cds alignment with highest coverage.
        for cds_aln in self._cds_aln_container.cds_repository:
            if best_cds_aln == None or self._get_coverage(cds_aln) > self._get_coverage(best_cds_aln):
                best_cds_aln = cds_aln

        #TODO: label best cds so it is not searched again (or move it to another repository?)
        #TODO: remove reads of best cds from all other cdss


    def _get_coverage(self, cds_aln):
        """ Returns
        @param (CdsAlignment) cds_aln
        @return coverage
        """
        # If coverage was not calculated before, calculate it and remember it for later.
        if not (cds_aln in self._coverages):
            self._coverages[cds_aln] = self._calc_coverage(cds_aln)

        return self._coverages[cds_aln]
            

    def _calc_coverage(self, cds_aln):
        """
        @param (CdsAlignment) cds_aln
        """
        # Aligned region is part of a read that intersects with cds.
        # Coverage is calculated as sum of lengths of aligned regions divided by number of aligned regions.
        for aln_reg in cds_aln.aligned_regions:
            pass



                
            
