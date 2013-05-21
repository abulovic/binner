import sys, os
sys.path.append(os.getcwd())

from solver.determine_host  import determine_host
from data.containers.read   import ReadContainer
from ncbi.db.access         import DbQuery

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:\npython determine_host_test.py <INPUT ALIGNMENT FILE>"
        sys.exit(-1)

    alignment_file = sys.argv[1]
    assert (os.path.isfile(alignment_file))

    db_query = DbQuery()
    read_cont = ReadContainer()
    read_cont.populate_from_aln_file(alignment_file)

    (host_taxid, host_read_cnt, read_cont) = determine_host(read_cont)
    
    if host_taxid:
	print "Host taxid estimated to be: %d" % (host_taxid)
    else:
        print "No non-microbial organisms detected."
