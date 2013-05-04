import Read2CDSSolver.*

class GreedySolver (Read2CDSSolver):
    """ Implementation of Read2CDSSolver that uses greedy algorithm to decide to which CDS does read belong.
    CDS with best coverage is taken and all its reads are assigned to it and removed from other CDSs. 
    Coverage of other CDSs is then updated. Process is repeated until there are no more reads left.
    """
    pass
