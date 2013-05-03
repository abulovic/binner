from solvers.Solver 		import Solver

from data.containers.read 	import ReadContainer
from data.containers.cdsaln import CdsAlnContainer

class HighestScoreSolver (Solver):

	def __init__ (self, alignment_file):

		readContainer   = ReadContainer.Instance()
		cdsAlnContainer = CdsAlnContainer.Instance()
		super(HighestScoreSolver, self).__init__ (readContainer, cdsAlnContainer)

		self.readContainer.populate_from_aln_file (alignment_file)
