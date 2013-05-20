from collections import defaultdict

from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access     import DbQuery 


def remove_host_reads (read_container, tax_tree, gi2taxid):
    '''
    Removes host reads from the read container.
    Host reads are considered to be all the reads which
    have the best alignment mapped to potential host. 
    Potential host is any organism from animalia kingdom.
    Annotes all the read alignments as potential host
    alignments or not.
    @param read_container (ReadContainer)
    @param tax_tree (TaxTree)
    @param gi2taxid (dict) key: gi (int), value: taxid (int) 
    @return (read_container, host_read_cnt) (ReadContainer, int)
    '''

    host_read_cnt = 0

    for read in read_container.fetch_all_reads(format=iter):
        read_alignments = read.get_alignments()
        if not len(read_alignments):
            continue
        # sort alignments by alignment score
        sorted_alignments = sorted (read_alignments, key=lambda location: location.score, reverse=True)
        # if best alignment is host alignment, remove it
        best_aln = sorted_alignments[0]
        try:
            best_aln_taxid = gi2taxid [best_aln.genome_index]
            if (tax_tree.is_child (best_aln_taxid, tax_tree.animalia)):
                # del read_container.read_repository[read.id]
                read.set_active(False)
                host_read_cnt += 1
        except KeyError, e:
            print "solver/determine_host", e
        
        # set all host alignments inactive
        for read_aln in read_alignments:
     	    if not gi2taxid.has_key(read_aln.genome_index):
                print "NOT IN NCBITAX: %d" % read_aln.genome_index
                read_aln.set_active(False)
                continue

            taxid = gi2taxid [read_aln.genome_index]
            if tax_tree.is_child (taxid, tax_tree.animalia):
                read_aln.set_active(False)
                # mark read alignment as potential host
                read_aln.set_potential_host_status(True)

    return (read_container, host_read_cnt)


def determine_host(read_container):
    ''' Method serves to determine host among all the read alignments.
        An organism is considered host if it is a descendent of kingdom Animalia.
        Method counts the most frequent organism and declares it host.
        Filters read container to remove all reads best aligned to potential host.
        Potential host is anything from animalia kingdom.
        ! Precondition: All the alignments have been loaded into read container.
        @param (ReadContainer) read container (loaded with read data)
        @return (host_taxid, host_read_cnt) (int, int)
    '''
    dbquery = DbQuery()
    tax_tree = TaxTree()

    reads = read_container.fetch_all_reads(format=iter)
    taxids_cnt = defaultdict(int)
    gis_cnt    = defaultdict(int)

    # find out how many times each GI is reported
    # in the alignments
    for read in reads:
        for read_aln in read.alignment_locations:
            gis_cnt[read_aln.genome_index] += 1

    # find gi <-> taxid mapping using ncbi database
    gi2taxid = dbquery.get_taxids (gis_cnt.keys(), format=dict)
    # deactivate reads that map to potential host
    (read_container, host_read_cnt) =  remove_host_reads (read_container, tax_tree, gi2taxid)
    
    # calculate how many times each taxid is reported
    for (gi, taxid) in gi2taxid.items():
        taxids_cnt[taxid] += gis_cnt[gi]

    # find the most frequent taxid from animalia kingdom
    host_taxid = None
    # sort taxids by occurence 
    sorted_taxid_cnt = sorted (taxids_cnt.items(), key= lambda x: x[1], reverse=True)
    for (taxid, cnt)  in sorted_taxid_cnt:
    	if tax_tree.is_child(taxid, tax_tree.animalia):
            host_taxid = taxid
            break

    return (host_taxid, host_read_cnt, read_container)
