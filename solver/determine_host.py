from collections import defaultdict

from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access     import DbQuery

class HostData (object):
    pass

def determine_host(read_container):
    ''' Method serves to determine host among all the read alignments.
        An organism is considered host if it is a descendent of kingdom Animalia.
        Method counts the most frequent organism and declares it host.
        ! Precondition: All the alignments have been loaded into read container.
        @param (ReadContainer) read container (loaded with read data)
        @return (HostData)
    '''
    dbquery = DbQuery()
    tax_tree = TaxTree()

    reads = read_container.fetch_all_reads()
    taxids_cnt = defaultdict(int)
    gis_cnt    = defaultdict(int)

    # find out how many times each GI is reported
    # in the alignments
    for read in reads:
        for read_aln in read.alignment_locations:
            gis_cnt[read_aln.genome_index] += 1

    # find gi <-> taxid mapping using ncbi database
    gi2taxid = dbquery.get_taxids (gis_cnt.keys(), format=dict)
    for (gi, taxid) in gi2taxid:
        taxids_cnt[taxid] += gis_cnt[gi]

    # find the taxid that has been reported the most
    max_cnt = 0
    max_taxid = None
    for (taxid, cnt) in taxids_cnt:
        if cnt > max_cnt:
            max_cnt = cnt
            max_taxid = taxid

    return taxid

    








