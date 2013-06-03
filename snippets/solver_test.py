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

if __name__ == '__main__':

    Logger("LOGFILE")

    if (len(sys.argv) < 5):
        print "Solver usage: python populate_containers.py <INPUT_ALN_FILE> <DATASET_DESC_XML_FILE> <SOLUTION_XML_OUTPUT_FILE> <STATS_OUTPUT_DIRECTORY>"
        sys.exit(-1)
    aln_file = sys.argv[1]
    dataset_xml_file = sys.argv[2]
    solution_xml_output_file = sys.argv[3]
    stats_dir = sys.argv[4]

    log.info("I got the input file!")

        
        # ---------------------- Initialize Solver --------------------- #

    greedySolver    = GreedySolver()
    taxonomySolver  = SimpleTaxonomySolver() 
    solver = Solver(determine_host, greedySolver, taxonomySolver)
                        

        # ---------------------- Run Solver --------------------- #
    
    solver.generateSolutionXML(aln_file, dataset_xml_file, 
                               solution_xml_output_file, stats_dir)
