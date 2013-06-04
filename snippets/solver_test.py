import sys, os
sys.path.append(os.getcwd())

from ncbi.db.access         import DbQuery
from data.containers.record import RecordContainer    
from data.containers.read   import ReadContainer    
from data.containers.cdsaln import CdsAlnContainer

from solver.read2cds.Read2CDSSolver import Read2CDSSolver
from solver.read2cds.GreedySolver import GreedySolver
from solver.taxonomy.SimpleTaxonomySolver import SimpleTaxonomySolver
from solver.Solver import Solver

from solver.determine_host import determine_host

import statistics.statistics as stats
from utils.logger import Logger
import time

if __name__ == '__main__':

    Logger("LOGFILE")

    if (len(sys.argv) < 4):
        print "Solver usage: python populate_containers.py <INPUT_ALN_FILE> <DATASET_DESC_XML_FILE> <SOLUTION_XML_OUTPUT_FILE>"
        sys.exit(-1)
    aln_file = sys.argv[1]
    dataset_xml_file = sys.argv[2]
    solution_xml_output_file = sys.argv[3]

    log.info("I got the input file!")

        # # ---------------------- Initialize containers --------------------- #

        # # Enable database access
        # dbQuery = DbQuery()

        # # Create containers
        # recordCont = RecordContainer.Instance()
        # recordCont.set_db_access(dbQuery)

        # readCont   = ReadContainer.Instance()
        # cdsAlnCont = CdsAlnContainer.Instance()

        # readCont.populate_from_aln_file(aln_file)

        # print "passed container initialization!"
        
        # ---------------------- Initialize Solver --------------------- #

    greedySolver    = GreedySolver()
    taxonomySolver  = SimpleTaxonomySolver() 
    solver = Solver(determine_host, greedySolver, taxonomySolver)
                        

        # ---------------------- Run Solver --------------------- #
    start_total = time.time()
    
    solver.generateSolutionXML(aln_file, dataset_xml_file, solution_xml_output_file)

    log.info("Successfully initialized solver!")

    end_total = time.time()
    elapsed_time_total = end_total - start_total
    print ("TOTAL - \t\telapsed time: %.2f" % elapsed_time_total)
        
	# fill_containers (aln_file)

        # -------------------- Test stats methods ----------------------- #
'''
    read_container = ReadContainer.Instance()
    cds_aln_container = CdsAlnContainer.Instance()
	
    no_alns = stats.num_reads_with_no_alignments(read_container)
    print "Reads with no alignments: %d" % no_alns
    print "Number of reads: %d" % stats.num_reads(read_container)

    print "Number of reads with no aligned cdss: %d" % \
	  stats.num_reads_with_no_aligned_cdss(read_container, cds_aln_container)

    print "Number of reads with host and parasit alignments: %d" % \
	      stats.num_reads_with_host_and_parasit_alignments(cds_aln_container)

    print "Number of reads with multiple aligned cdss: %d" % \
	      stats.num_reads_with_multiple_aligned_cdss(cds_aln_container)

    average, deviation = stats.calc_average_cds_coverage(cds_aln_container)
    print "Average and deviation of cds coverage: %f %f" % (average, deviation)
	
    more_sublocs = stats.num_reads_with_multiple_mapped_cds_sublocations(read_container)
    print "Reads aligned to more sublocs of CDS: %d" % more_sublocs
'''
