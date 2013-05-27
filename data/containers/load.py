'''
:Date: 13.05.2013.
:Author: Ana Bulovic <bulovic.ana@gmail.com> 
'''

from data.containers.read   import ReadContainer
from data.containers.record import RecordContainer
from data.containers.cdsaln import CdsAlnContainer
from ncbi.db.mock_db_access import MockDbQuery

def fill_containers (alignment_file, db_access):
    '''
    Populates read, record and CDS alignment container.

    :param alignment_file: path to Binner input alignment file
    :param db_acccess: database access object. Can be :class:`ncbi.db.access.DqQuery`
        or :class:`ncbi.db.mock_db_access.MockDbQuery` for testing purposes

    :rtype: tuple(:class:`data.containers.read.ReadContainer`, 
            :class:`data.containers.record.RecordContainer`, 
            :class:`data.containers.cdsaln.CdsAlnContainer`)
    '''

    read_cont   = ReadContainer()
    record_cont = RecordContainer()
    record_cont.set_db_access(db_access)
    cdsaln_cont = CdsAlnContainer()

#   1. Load all the information available in the alignment file
    read_cont.populate_from_aln_file(alignment_file)
#   2. Fetch all the records reported in the alignment file from the database
    record_cont.populate(read_cont)
#   3. Find to which coding sequences reads map
    read_cont.populate_cdss(record_cont)
#   4. Populate Cds Alignment container
    cdsaln_cont.populate(read_cont)

    return (read_cont, record_cont, cdsaln_cont)
