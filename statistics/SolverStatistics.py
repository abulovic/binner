import statistics as stats
from ComparisonData import ComparisonData
import cPickle as pickle
from datetime import datetime
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
    Number of cdss in cds alignment container.    
    (int) num_cdss_with_no_alns  Only in phases 2, 3, 4.
    Number of cdss in cds alignment container
    with no active aligned regions.
    (int) num_cds_alns  Only in phases 2, 3, 4.
    Number of active aligned regions in all cdss.
    """
    

    def __init__(self):
        self.time                   = datetime.time(datetime.now())

        self.num_missing_records    = None
        self.num_reads              = None
        self.num_reads_with_no_alns = None
        self.proteins               = None
        self.taxs                   = None
        self.num_alns_to_record_and_cds = None

        self.num_read_alns          = None
        self.num_host_read_alns     = None
        self.num_cdss               = None
        self.num_cdss_with_no_alns  = None
        self.num_cds_alns           = None

    def shortStr(self):
        """ Returns string representation containing only simple sttributes,
        which can be easily read.
        """
        res = ""
        for attr in ["time", "num_reads", "num_reads_with_no_alns", 
                     "num_read_alns", "num_host_read_alns",
                     "num_cdss", "num_cdss_with_no_alns",
                     "num_cds_alns", "num_missing_records"]:
            if getattr(self, attr) != None:
                res += attr + ": " + str(getattr(self, attr)) + "\n"
        for attr in ["proteins"]:
            if getattr(self, attr) != None:
                res += "num_" + attr + ": " + str(len(getattr(self, attr))) + "\n"
        return res
        

    def __str__(self):
        res = self.shortStr()
        for attr in ["proteins", "taxid2cdss"]:
            if getattr(self, attr) != None:
                res += attr + ": " + str(getattr(self, attr)) + "\n"
        res += "\n// ---------------------- Number of alignments to each record -------------------- //\n\n"
        # Matija - number of alignments to each record and CDS
        for record_stats in self.num_alns_to_record_and_cds.values():
            res += str(record_stats) + "\n"
        return res



class SolverStatistics:
    """ Stores statistical data about solver, for different phases (5 of them).
    (dict) phaseData  Dictionary where key is phase number(int) and value is (StatData). 
                      phaseData[i] contains statistical data from phase i.
    (dict) comparison_data  Dictionary where key is phase number(int) and 
                            value is (ComparisonData). 
    """
    phaseDescr = ("after preprocess", "after determine host", "after Read2cdsSolver", 
                  "after TaxonomySolver", "after generating xml output")

    def __init__(self, filepath=None):
        """ If file path is given then statistical data is loaded from file.
        @param (string) filepath
        """
        if (filepath == None):
            self.phaseData = dict()
            self.comparison_data = dict()
        else:
            infile = open(filepath, 'r')
            self.phaseData, self.comparison_data = pickle.load(infile)
            


    def collectPhaseData(self, phase, record_cont, read_cont, cds_aln_cont=None,
                         taxid2cdss=None, solution_data=None):
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
        @param (dict) taxid2cdss  Only in phase 4.
        @param ([Organism]) solution_data  Data to be compared against.
                                           Comparison will be stored in comparison_data.

        """        
        if (cds_aln_cont == None and phase != 1):
            raise ValueError("cds_aln_container can be None only for phase 1!")

        statData = StatData()
        
        statData.num_reads              = stats.num_reads(read_cont)
        statData.num_reads_with_no_alns = stats.num_reads_with_no_alns(read_cont)
        statData.proteins               = read_cont.get_protein_ids(phase != 1)
        #statData.taxs                  = NIJE IMPLEMENTIRANO
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

        if solution_data is not None:
            self.comparison_data[phase] = ComparisonData(solution_data, record_cont, 
                                                         read_cont, cds_aln_cont, taxid2cdss)


    def toFile(self, filepath, directory=""):
        """ Statistical data is saved to file using pickle.
        It can be reconstructed from that file if filepath
        is passed to constructor.
        @param (string) filepath
        @param (string) directory  Path to directory, no delimiter at end.
        """
        if directory != "":
            if not os.path.isdir(directory):
                os.makedirs(directory)
            filepath = directory + "/" + filepath
        outfile = open(filepath, 'w')
        pickle.dump((self.phaseData, self.comparison_data), outfile)

    def __str__(self):
        res = ""
        for (phase, statData) in self.phaseData.items():
            res += "\nPhase " + str(phase) + " (" + SolverStatistics.phaseDescr[phase-1] + "):\n"
            res += statData.shortStr()
            res += "---- Comparison data ----\n"
            if phase in self.comparison_data:
                res += self.comparison_data[phase].shortStr()
        return res

    def writeToFiles(self, stats_dir):
        """ Creates a directory and in it one file for each phase.
        In each file statistic data for that phase is written in human readable format.
        @param (String) stats_dir Directory name (Can be path).
        """
        if not os.path.isdir(stats_dir):
            os.makedirs(stats_dir)
        for (phase, statData) in self.phaseData.items():
            txt_file = open(stats_dir + "/phase_" + str(phase) + ".txt", "w")
            txt_file.write(str(statData))
            txt_file.close()
