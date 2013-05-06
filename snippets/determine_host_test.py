import sys, os
sys.path.append(os.getcwd())

from solver.determine_host import determine_host
from data.containers.load import initialize_containers

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:\npython determine_host_test.py <INPUT ALIGNMENT FILE>"
        sys.exit(-1)

    alignment_file = sys.argv[1]
    assert (os.path.isfile(alignment_file))

    (read_cont, record_cont, cds_aln_cont) = initialize_containers()
    read_cont.populate_from_aln_file(alignment_file)

    host_taxid = determine_host(read_cont)

    print "Host taxid estimated to be: %d" % (host_taxid)
