import statistics.statistics as stats

class SolverStatistics:
    def __init__(self):
        """
        self.phaseData: dictionary where key is phase number(int)
                        and value is (StatData). phaseData[i] contains
                        statistic data from phase i.
        """
        self.phaseData = dict()


    def collectPhaseData(self, phase, record_cont, read_cont, cds_aln_cont):
        """ Collects statistical data specific for certain phase in Solver.
        Data for specific phase is stored in .phaseData[phase].
        There are 5 phases, which means that this functions should be called 5 times during Solver.
        Collection for phase 1 should be run after preprocess but before determineHost().
        Collection for phase 2 should be run after determineHost().
        Collection for phase 3 should be run after Read2cdsSolver.
        Collection for phase 4 should be run after TaxonomySolver.
        Collection for phase 5 should be run after generating xml output.
        @param (int) phase  Number of phase for which data will be collected.
                            It can be 1, 2, 3, 4 or 5.
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont  Should and can be null for phases 1 and 2.
        """        
        statData = new StatData()
        
        statData.num_reads              = stats.num_reads(read_cont)
        statData.num_reads_with_no_alns = stats.num_reads_with_no_alns(read_cont)
        #statData.proteins              = ???  JERKO
        #statData.taxs                  = ???  JERKO
        #statData.record_alns           = ???  Matija
        #statData.cds_alns              = ???  Matija, zar ovo moze u prvoj fazi?
        statData.num_read_alns          = stats.num_read_alns(read_cont)
        
        #if phase == 1:
        #    statData.num_missing_records   = ???  JERKO
        #if phase == 2:
        #    statData.num_host_read_alns = stats.num_host_read_alns(read_cont)   Martin dovrsiti
        if phase in [2,3,4]:
            statData.num_cdss = stats.num_cdss(cds_aln_cont)
            statData.num_cdss_with_no_alns = stats.num_cdss_with_no_alns(cds_aln_cont)
            statData.num_cds_alns = stats.num_active_aligned_regions(cds_aln_cont)

        self.phaseData[phase] = statData

    
    
    class StatData:
        """ Stores statistic data about solver.
        Depending on phase, some attributes may be None.
        (?) time  Time the moment before this data was collected.
        (int) num_missing_records  Only in phase 1.
        (int) num_reads
        (int) num_reads_with_no_alns  Number of read with no read alignments.
        (?) proteins  Number of proteins and protein ids.
        (?) taxs  Num of taxes and tax ids.
        (?) record_alns  For each record: Record id and number of 
                         read alignments for that record.
        (?) cds_alns  For each cds: protein id and number of aligned regions.
        (int) num_read_alns  Number of read alignments.
        (int) num_host_read_alns  Only in phase 2.
                                  Number of read alignments that are determined
                                  as host alignments.
        (int) num_cdss  Only in phases 2, 3, 4.
                        Number of cdss in cds alignment container.    IS THIS WHAT WE REALLY WANT/NEED?
        (int) num_cdss_with_no_alns  Only in phases 2, 3, 4.
                                     Number of cdss in cds alignment container
                                     with no active aligned regions.
        (int) num_cds_alns  Only in phases 2, 3, 4.
                            Number of active aligned regions in all cdss.
        """
        def __init__(self):
            self.time                   = None    # TODO: should set itself automatically in this line.

            self.num_missing_records    = None
            self.num_reads              = None
            self.num_reads_with_no_alns = None
            self.proteins               = None    # Ovo jerko sredit/popravit
            self.taxs                   = None    # Ovo jerko sredit/popravit
            self.record_alns            = None    # Matija
            self.cds_alns               = None    # Matija
            self.num_read_alns          = None
            self.num_host_read_alns     = None
            self.num_cdss               = None    # Jel to ono sto zelimo?
            self.num_cdss_with_no_alns  = None    # Jel to ono sto zelimo?
            self.num_cds_alns           = None

            
