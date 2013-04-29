from data.containers.read 	import ReadContainer
from data.containers.record import RecordContainer
from data.containers.cdsaln import CdsAlnContainer
from ncbidb.access 			import DbQuery

def fill_containers (alignment_file):

    # enable database access
    dbQuery = DbQuery()
    # create containers
    recordCont = RecordContainer.Instance()
    recordCont.set_db_access(dbQuery)
    readCont   = ReadContainer.Instance()
    cdsAlnCont = CdsAlnContainer.Instance()

    # --------------------------- Populate readCont ---------------------------------- #

    # Populate from the read container
    readCont.populate_from_aln_file(alignment_file)

    # Debugging output
    print "readCont populated!"
    print ( "len(readCont): %d" % len(readCont.read_repository) )

    # --------------------------- Populate cdsAlnCont ---------------------------------- #

    # Populate cdsAlnCont using readCont
    cdsAlnCont.populate(readCont);

    return (readCont, recordCont, cdsAlnCont)
