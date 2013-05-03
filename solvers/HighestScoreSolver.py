from solvers.Solver 		import Solver

from data.containers.load	import initialize_containers

class HighestScoreSolver (Solver):

	def __init__ (self, alignment_file):

		(readCont, recordCont, cdsAlnCont) = initialize_containers()
		super(HighestScoreSolver, self).__init__ (readCont, cdsAlnCont)

		self.readContainer.populate_from_aln_file (alignment_file)
