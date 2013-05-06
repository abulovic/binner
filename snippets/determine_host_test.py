import sys, os
sys.path.append(os.getcwd())

from solver.taxonomy.determine_host import determine_host
from data.containers.read           import ReadContainer

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:\npython determine_host_test.py <INPUT ALIGNMENT FILE>"
        sys.exit(-1)

    alignment_file = sys.argv[1]
    assert (os.path.isfile(alignment_file))

    read_cont = ReadContainer.Instance()
    read_cont.populate_from_aln_file(read_cont)

    host_taxid = determine_host(read_cont)

    print "Host taxid estimated to be: %d" % (host_taxid)