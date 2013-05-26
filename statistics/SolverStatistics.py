class SolverStatistics:
    def __init__(self):
        """
        self.phases: dictionary where key is phase number(int)
                     and value is (Phase)
        """
        self.phases = dict()


    def collectPhase1Data(record_cont, read_cont):
        """
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        """
        return None
    
    def collectPhase2Data(record_cont, read_cont, cds_aln_cont):
        """
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase3Data(record_cont, read_cont, cds_aln_cont):
        """
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase4Data(record_cont, read_cont, cds_aln_cont):
        """
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    def collectPhase5Data(record_cont, read_cont, cds_aln_cont):
        """
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        """
        return None

    
    class Phase:
        def __init__(self):
            self.time = None
