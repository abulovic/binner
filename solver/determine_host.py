from collections import defaultdict

from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access     import DbQuery
from data.containers.load import 


def remove_host_reads (read_container, tax_tree, gi2taxid):

    for (read_id, read) in read_container.read_repository:
        # sort alignments by alignment score
        sorted_alignments = sorted (read.alignment_locations, key=location.score)
        # if best alignment is host alignment, remove it
        best_aln = sorted_alignments[0]
        best_aln_taxid = gi2taxid [best_aln.genome_index]
        if (tax_tree.is_child (best_aln_taxid, tax_tree.animalia)):
            del read_container.read_repository[read_id]
        # set all host alignments inactive
        for read_aln in read.alignment_locations:
            taxid = gi2taxid [read_aln.genome_index]
            if tax_tree.is_child (taxid, tax_tree.animalia):
                read_aln.set_active(False)

        return read_container


def determine_host(read_container):
    ''' Method serves to determine host among all the read alignments.
        An organism is considered host if it is a descendent of kingdom Animalia.
        Method counts the most frequent organism and declares it host.
        Filters read container to remove all reads best aligned to potential host.
        Potential host is anything from animalia kingdom.
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

    # filter read container. Read container iterator no longer valid
    # after filtering
    reads = None
    read_container = filter_read_container (read_container, tax_tree, gi2taxid)
    

    for (gi, taxid) in gi2taxid.items():
        taxids_cnt[taxid] += gis_cnt[gi]

    # find the taxid that has been reported the most
    max_cnt = 0
    max_taxid = None
    for (taxid, cnt) in taxids_cnt.items():
        if cnt > max_cnt:
            max_cnt = cnt
            max_taxid = taxid

    return taxid