import sys, os
import copy
sys.path.append(os.getcwd())

from ncbi.db.access import DbQuery
from solver.read2cds.GreedySolver import GreedySolver
from solver.read2cds.Read2CDSSolver import Read2CDSSolver
from data.containers.record import RecordContainer
from data.containers.read import ReadContainer
from data.containers.cdsaln import CdsAlnContainer

db_query = DbQuery()

# create containers
record_container = RecordContainer()
record_container.set_db_access(db_query)

read_container = ReadContainer()
read_container.populate_from_aln_file("example_data/2reads.in")

record_container.populate(read_container)
read_container.populate_cdss(record_container)

cds_aln_container = CdsAlnContainer()
cds_aln_container.populate(read_container)

#print cds_aln_container


r2c_solver = GreedySolver()
r2c_solver.map_reads_2_cdss(cds_aln_container)

print "Consistency test result: ", Read2CDSSolver.test_cds_alignment_container_consistency(cds_aln_container)

#print "------------------------------------------------"
#print cds_aln_container


r2c_solver.remove_cds_and_remap_reads(cds_aln_container.cds_repository.values()[0])
print "Consistency test result: ", Read2CDSSolver.test_cds_alignment_container_consistency(cds_aln_container)

#print "------------------------------------------------"
#print cds_aln_container
