import sys, os
sys.path.append(os.getcwd())

from ncbi.db.access import DbQuery
from solver.read2cds.GreedySolver import GreedySolver
from data.containers.record import RecordContainer
from data.containers.read import ReadContainer
from data.containers.cdsaln import CdsAlnContainer

db_query = DbQuery()

# create containers
record_container = RecordContainer.Instance()
record_container.set_db_access(db_query)

read_container = ReadContainer.Instance()
read_container.populate_from_aln_file("example_data/2reads.in")

cds_aln_container = CdsAlnContainer.Instance()
cds_aln_container.populate(read_container)

r2c_solver = GreedySolver()
r2c_solver.map_reads_2_cdss(cds_aln_container)

print "gotov"
