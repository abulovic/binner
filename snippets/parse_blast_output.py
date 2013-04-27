import sys

from formats.blast2input import BLASTParser

if __name__ == '__main__':

	if (len(sys.argv) != 4):
	    print "Usage:\npython load_blast.py <BLAST_ALIGNMENT_FILE> <OUTPUT_FILE> <BLAST_OUTFMT>"
	    sys.exit(-1)
	    
	alignment_fname = sys.argv[1]
	output_fname    = sys.argv[2]
	blast_outfmt    = sys.argv[3]

	print "Loading alignment file:  {0}".format(alignment_fname)
	print "Alignment file format:   {0}".format(blast_outfmt)

	parser = BLASTParser(blast_outfmt)
	parser.convert_file (alignment_fname, output_fname)
