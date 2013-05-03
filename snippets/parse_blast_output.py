# Transform BLAST output to input format specification.

import sys, os
sys.path.append(os.getcwd())
from formats.blast2input import BLASTParser

if __name__ == '__main__':

	if (len(sys.argv) < 3):
	    print "Usage:\npython load_blast.py <BLAST_ALIGNMENT_FILE> <OUTPUT_FILE> [BLAST_OUTFMT]"
	    print "  Default BLAST format: "
	    print "  qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"
	    sys.exit(-1)
	    
	alignment_fname = sys.argv[1]
	output_fname    = sys.argv[2]
	if len(sys.argv) != 4:
		blast_outfmt = None
	else:
		blast_outfmt = sys.argv[3]

	print "Loading alignment file:  {0}".format(alignment_fname)
	print "Alignment file format:   {0}".format(blast_outfmt)

	parser = BLASTParser(blast_outfmt)
	parser.convert_file (alignment_fname, output_fname)
