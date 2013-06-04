class ComparisonData (object):
    """ This class contains data comparison between final result and
        one of solver phases.
    """

    def __init__(self, stat_data, solution_data):
        """ Takes statistic data of solver phase and solution data,
        compares them and stores comparison result in self.
        @param (StatData) stat_data  Contains data of specific phase.
        @param (SolutionData) solution_data  Contains solution data.
        """
        # Ovdje izracunati rezultate usporedbe i pospremiti u atribute.
        # One koji se ne mogu izracunati jer fale podaci postavi se na None.
        self.cds_comparison = None
        self.organism_comparison = None
