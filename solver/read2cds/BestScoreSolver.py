# @author: Martin Sosic, sosic.martin@gmail.com
from Read2CDSSolver import Read2CDSSolver
from utils.location import Location

class BestScoreSolver (Read2CDSSolver):
    """ Simple implementation of Read2CDSSolver that does following for each read:
    Takes alignment with largest score, maps it to CDS to which it aligns
    and deactivates all other alignments of that read.
    """

    def __init__(self):
        super(BestScoreSolver, self).__init__()

        
    def map_reads_2_cdss(self, cds_aln_container):
        """ @overrides
        """
        super(BestScoreSolver, self).map_reads_2_cdss(cds_aln_container)

        # For each read, go through all belonging activated aligned regions,
        # find one with highest score and deactivate all others.
        for (read_id, cds_alns) in self._cds_aln_container.read2cds.items(): # for each read
            best_aln_reg = None
            # Find active aligned region with highest score and deactivate them all
            for cds_aln in cds_alns: # for each aligned region
                aln_reg = cds_aln.aligned_regions[read_id]
                if (aln_reg.active):
                    if (best_aln_reg == None or aln_reg.score > best_aln_reg.score):
                        best_aln_reg = aln_reg
                    aln_reg.active = False
            # Activate aligned region with highest score
            best_aln_reg.active = True

