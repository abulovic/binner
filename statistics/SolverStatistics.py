class SolverStatistics:
    def __init__(self):
        """
        self.phaseData: dictionary where key is phase number(int)
                        and value is (StatData). phaseData[i] contains
                        statistic data from phase i.
        """
        self.phaseData = dict()


    def collectPhase1Data(record_cont, read_cont):
        """ Should be run after preprocess but before determineHost().
        Data is stored in .phaseData[1].
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        """
        
        return None
    
    def collectPhase2Data(record_cont, read_cont, cds_aln_cont):
        """ Should be run after determineHost().
        Data is stored in .phaseData[2].
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase3Data(record_cont, read_cont, cds_aln_cont):
        """
        Data is stored in .phaseData[3].
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase4Data(record_cont, read_cont, cds_aln_cont):
        """
        Data is stored in .phaseData[4].
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase5Data(record_cont, read_cont, cds_aln_cont):
        """
        Data is stored in .phaseData[5].
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    
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
        (?) cds_alns  Only in phases 3, 4, 5. 
                      For each cds: protein id and number of aligned regions.
        (int) num_read_alns  Number of read alignments.
        (int) num_host_read_alns  Only in phase 2.
                                  Number of read alignments that are determined
                                  as host alignments.
        (int) num_cdss  Only in phases 3, 4.
                        Number of cdss in cds alignment container.    IS THIS WHAT WE REALLY WANT/NEED?
        (int) num_cdss_with_no_alns  Only in phases 3, 4.
                                     Number of cdss in cds alignment container
                                     with no active aligned regions.
        """
        def __init__(self):
            self.time =                  None    # TODO: should set itself automatically in this line.

            self.num_missing_records =   None
            self.num_reads =             None
            self.num_read_with_no_alns = None
            self.proteins =              None    # Ovo jerko sredit/popravit
            self.taxs =                  None    # Ovo jerko sredit/popravit
            self.record_alns =           None    # Matija
            self.cds_alns =              None    # Matija
            self.num_read_alns =         None
            self.num_host_read_alns =    None
            self.num_cdss =              None    # Jel to ono sto zelimo?
            self.num_cdss_with_no_alns = None    # Jel to ono sto zelimo?

            
