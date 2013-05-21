
import sys, os
sys.path.append(os.getcwd())
from data.containers.load import fill_containers
from ncbi.db.mock_db_access import MockDbQuery

# input file: E:\\Projects\\Metagenomics\\data\\microbial\\6input_format.txt

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        print "Usage: python populate_containers.py <INPUT_ALN_FILE>"
        sys.exit(-1)
    aln_file = sys.argv[1]
    db_access = MockDbQuery (aln_file)
    fill_containers (aln_file, db_access)

