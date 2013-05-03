import sys,os
sys.path.append(os.getcwd())
from solvers.HighestScoreSolver import HighestScoreSolver

if __name__ == '__main__':
	if (len(sys.argv) < 2):
		print "Usage: python test_HSS.py <ALIGNMENT_FILE>"
		sys.exit(-1)
	aln_file = sys.argv[1]

	hss = HighestScoreSolver(aln_file)