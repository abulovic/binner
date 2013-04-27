
import sys
from data.containers import fill_containers
from data.containers import ReadContainer
from data.containers import RecordContainer
from data.containers import CdsAlnContainer

# input file: E:\\Projects\\Metagenomics\\data\\microbial\\6input_format.txt

if __name__ == '__main__':
	aln_file = sys.argv[1]
	fill_containers (aln_file)

