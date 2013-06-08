class ComparisonData (object):
    """ This class contains data comparison between final result and
        one of solver phases.
    """

    def __init__(self, solution_data, record_cont, read_cont, cds_aln_cont=None,
                 taxid2cdss=None):
        """ Takes solution data and data that represents current state of solver,
        compares them and stores comparison result in self.
        @param (SolutionData) solution_data  Contains solution data.
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        @param (dict) taxid2cdss  Result of TaxonomySolver
        """

        # Ovdje izracunati rezultate usporedbe i pospremiti u atribute.
        # One koji se ne mogu izracunati jer fale podaci postavi se na None.
        self.cds_comparison = None
        self.organism_comparison = None

        # ----------------------------- Read stats for every organism ----------------------------- #

        # For every organism
            # Store total number of reported reads
            # For every read reported in solution XML:
                # If we potentially reported it -> counter ++

        organism_read_stats = {};
        total_reads_in_sol = 0;
        total_reads_from_sol_we_found = 0;

        for organism in solution_data:

            total_reported_reads_in_organism = len(organism.reads)

            for read_id in organism.reads:
                for read_aln in read_cont.read_repository[read_id]:
                    pass
                


