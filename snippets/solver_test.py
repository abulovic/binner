import sys, os
sys.path.append(os.getcwd())

from ncbi.db.access         import DbQuery
from data.containers.record import RecordContainer    
from data.containers.read   import ReadContainer    
from data.containers.cdsaln import CdsAlnContainer

from solver.read2cds.Read2CDSSolver import Read2CDSSolver
from solver.read2cds.GreedySolver import GreedySolver
from solver.taxonomy.TaxonomySolver import TaxonomySolver
from solver.Solver import Solver

from solver.determine_host import determine_host

if __name__ == '__main__':

	if (len(sys.argv) < 2):
		print "Solver usage: python populate_containers.py <INPUT_ALN_FILE>"
		sys.exit(-1)
	aln_file = sys.argv[1]

        print "I got the input file!"

        # ---------------------- Initialize containers --------------------- #

        # Enable database access
        dbQuery = DbQuery()

        # Create containers
        recordCont = RecordContainer.Instance()
        recordCont.set_db_access(dbQuery)

        readCont   = ReadContainer.Instance()
        cdsAlnCont = CdsAlnContainer.Instance()

        readCont.populate_from_aln_file(aln_file)

        print "passed container initialization!"
        
        # ---------------------- Initialize Solver --------------------- #

        greedySolver    = GreedySolver()
        taxonomySolver  = TaxonomySolver() 
        solver = Solver(readCont, cdsAlnCont,
                        determine_host, greedySolver, taxonomySolver)
                        
        print "Successfully initialized solver!"
        
	# fill_containers (aln_file)
