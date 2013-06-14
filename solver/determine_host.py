from collections import defaultdict

from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access     import DbQuery 


def _mark_host_reads (reads, tax_tree, gi2taxid):
    '''
    Mark host reads in the read container.
    Host reads are considered to be all the reads which
    have the best alignment mapped to potential host. 
    Potential host is any organism from animalia kingdom.
    Annotes all the read alignments as potential host
    alignments or not.
    @param reads (iterator) Reads to check for host
    @param tax_tree (TaxTree)
    @param gi2taxid (dict) key: gi (int), value: taxid (int) 
    @return (host_read_count) (int)
    '''

    host_read_count = 0

    for read in reads:
        read_alignments = read.get_alignments()
        if not len(read_alignments):
            continue
        # sort alignments by alignment score
        sorted_alignments = sorted (read_alignments, key=lambda location: location.score, reverse=True)
        # if best alignment is host alignment, remove it
        best_aln = sorted_alignments[0]
        try:
            best_aln_taxid = gi2taxid [best_aln.genome_index]
            if (tax_tree.get_relevant_taxid(best_aln_taxid) in tax_tree.potential_hosts):
                # del read_container.read_repository[read.id]
                read.set_host_status(True)
                host_read_count += 1
            
        except KeyError, e:
            print "solver/determine_host", e
        
        # set all host alignments inactive
        for read_aln in read_alignments:
     	    if not gi2taxid.has_key(read_aln.genome_index):
                # print "NOT IN NCBITAX: %d" % read_aln.genome_index    # I think this is not needed
                read_aln.set_active(False)
                continue

            taxid = gi2taxid [read_aln.genome_index]
            if tax_tree.get_relevant_taxid(taxid) not in tax_tree.microbes:
                read_aln.set_active(False)
                read_aln.set_potential_host_status(True)

    return host_read_count

def _count_reported_taxids (reads, db_query):
    gis_container = defaultdict(int)
    taxids_container = defaultdict(int)
    # find out how many times each GI is reported
    # in the alignments
    for read in reads:
        for read_aln in read.alignment_locations:
            gis_container[read_aln.genome_index] += 1
    # find gi <-> taxid mapping using ncbi database
    gi2taxid = db_query.get_taxids (gis_container.keys(), format=dict)
    # calculate how many times each taxid is reported
    for (gi, taxid) in gi2taxid.items():
        taxids_container[taxid] += gis_container[gi]

    f = open('taxid_count.txt', 'w')
    for taxid, count in taxids_container.items():
        f.write("%d %d\n" % (int(taxid), int(count)))
    f.close()
    return (gi2taxid, taxids_container)


class HostDeterminator(object):
    def __init__(self, dbquery, tax_tree):
        self.dbquery = dbquery
        self.tax_tree = tax_tree

    def determine_host(self, reads):
        ''' Method serves to determine host among all the read alignments.
            An organism is considered host if it is a descendent of kingdom Animalia.
            Method counts the most frequent organism and declares it host.
            Filters read container to remove all reads best aligned to potential host.
            Potential host is anything from animalia kingdom.
            ! Precondition: All the alignments have been loaded into read container.
            @param (iterator) reads (loaded with read data)
            @return (host_taxid, host_read_cnt) (int, int)
        '''
         
        reads = list(reads)
        # how many times each taxid has been reported
        (gi2taxid, taxids_container)  = _count_reported_taxids(reads, self.dbquery)
        # deactivate reads that map to potential host
        host_read_count =  _mark_host_reads (reads, self.tax_tree, gi2taxid)
        
        # find the most frequent taxid from animalia kingdom
        host_taxid = None
        # sort taxids by occurence 
        sorted_taxid_cnt = sorted (taxids_container.items(), key= lambda x: x[1], reverse=True)
        for (taxid, cnt)  in sorted_taxid_cnt:
            if self.tax_tree.get_relevant_taxid(taxid) in self.tax_tree.potential_hosts:
                host_taxid = taxid
                break
    
        return (host_taxid, host_read_count)
