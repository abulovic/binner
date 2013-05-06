import sys, os
import copy
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

read = copy.deepcopy(read_container.read_repository.values()[0])
read.id = "fake_read"
for read_aln_loc in read.alignment_locations:
    read_aln_loc.read_id = read.id
read_container.read_repository[read.id] = read
print read_container.read_repository

cds_aln_container = CdsAlnContainer.Instance()
cds_aln_container.populate(read_container)

cds_aln_container.printSelf()


r2c_solver = GreedySolver()
r2c_solver.map_reads_2_cdss(cds_aln_container)

print "------------------------------------------------"
cds_aln_container.printSelf()


r2c_solver.remove_cds_and_remap_reads(cds_aln_container.cds_repository.values()[0])

print "------------------------------------------------"
cds_aln_container.printSelf()
