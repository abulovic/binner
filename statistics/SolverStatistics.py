import statistics as stats
import cPickle as pickle
import os


class StatData:
    """ Stores statistic data about solver.
    Depending on phase, some attributes may be None.
    (?) time  Time the moment before this data was collected.
    (int) num_missing_records  Only in phase 1.
    (int) num_reads
    (int) num_reads_with_no_alns  Number of read with no read alignments.
    (?) proteins  Number of proteins and protein ids.
    (?) taxs  Num of taxes and tax ids.

    ({record_id : RecordStats}) num_alns_to_record_and_cds  Number of alignments to each record and CDS.

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
        self.num_alns_to_record_and_cds = None

        self.num_read_alns          = None
        self.num_host_read_alns     = None
        self.num_cdss               = None    # Jel to ono sto zelimo?
        self.num_cdss_with_no_alns  = None    # Jel to ono sto zelimo?
        self.num_cds_alns           = None

    def shortStr(self):
        """ Returns string representation containing only simple sttributes,
        which can be easily read.
        """
        res = ""
        for attr in ["num_reads", "num_reads_with_no_alns", 
                     "num_read_alns", "num_host_read_alns",
                     "num_cdss", "num_cdss_with_no_alns",
                     "num_cds_alns", "num_missing_records", 
                     "proteins"]:
            if getattr(self, attr) != None:
                res += attr + ": " + str(getattr(self, attr)) + "\n"
        return res
        

    def __str__(self):
        res = self.shortStr()
        res += "\n// ---------------------- Number of alignments to each record -------------------- //\n\n"
        # Matija - number of alignments to each record and CDS
        for record_stats in self.num_alns_to_record_and_cds.values():
            res += str(record_stats) + "\n"
        return res



class SolverStatistics:
    """ Stores statistical data about solver, for different phases (5 of them).
    (dict) phaseData  Dictionary where key is phase number(int) and value is (StatData). 
                      phaseData[i] contains statistical data from phase i.
    """

    def __init__(self, filepath=None):
        """ If file path is given then statistical data is loaded from file.
        @param (string) filepath
        """
        if (filepath == None):
            self.phaseData = dict()
        else:
            infile = open(filepath, 'r')
            self.phaseData = pickle.load(infile)
         


    def collectPhaseData(self, phase, record_cont, read_cont, cds_aln_cont=None):
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
        @param (CdsAlnContainer) cds_aln_cont  Should and can be None for phase 1.
        """        
        if (cds_aln_cont == None and phase != 1):
            raise ValueError("cds_aln_container can be None only for phase 1!")

        statData = StatData()
        
        statData.num_reads              = stats.num_reads(read_cont)
        statData.num_reads_with_no_alns = stats.num_reads_with_no_alns(read_cont)
        statData.proteins               = read_cont.get_protein_ids(phase != 1)
        #statData.taxs                  = ???  JERKO - nacin na koji zasad dohvacam prespor
        statData.num_read_alns          = stats.num_read_alns(read_cont)
        statData.num_alns_to_record_and_cds      = stats.count_alns_to_record_and_cds(read_cont)

        if phase == 1:
            statData.num_missing_records = record_cont.get_num_missing_records_stats()
            statData.proteins = read_cont.get_protein_ids()
        if phase == 2:
            statData.num_host_read_alns = stats.num_inactive_read_alns(read_cont)
        if phase in [2,3,4]:
            statData.num_cdss = stats.num_cdss(cds_aln_cont)
            statData.num_cdss_with_no_alns = stats.num_cdss_with_no_alns(cds_aln_cont)
            statData.num_cds_alns = stats.num_active_aligned_regions(cds_aln_cont)

        self.phaseData[phase] = statData



    def toFile(self, filepath):
        """ Statistical data is saved to file using pickle.
        It can be reconstructed from that file if filepath
        is passed to constructor.
        @param (string) filepath
        """
        outfile = open(filepath, 'w')
        pickle.dump(self.phaseData, outfile)

    def __str__(self):
        res = ""
        for (phase, statData) in self.phaseData.items():
            res += "Phase " + str(phase) + ":\n"
            res += statData.shortStr()
        return res

    def writeToFiles(self):
        """ Creates a directory and in it one file for each phase.
        In each file statistic data for that phase is written in human readable format.
        """
        stats_dir = "solver_stats"
        if not os.path.isdir(stats_dir):
            os.makedirs(stats_dir)
        for (phase, statData) in self.phaseData.items():
            txt_file = open(stats_dir + "/phase_" + str(phase) + ".txt", "w")
            txt_file.write(str(statData))
            txt_file.close()

