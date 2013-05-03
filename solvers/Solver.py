
class Solver (object):

    """ Class which implements algorithm to determine host
        and products of non-host CDSs.

        Idea:   This class could be abstract - defines only methods 
                which should be implemented.

                This way we could implement multiple different algorithms
                and try them out easily.
    """

    # Constructor
    # 
    # @param readContainer      ReadContainer instance
    # @param cdsAlnContainer    CdsAlnContainer instacnce
    #
    #   NOTE: Although these are singletons, I added them just for the clarity
    #
    def __init__ (self, readContainer, cdsAlnContainer):
        self.readContainer = readContainer
        self.cdsAlnContainer = cdsAlnContainer
        
        # Populate readContainer

        # Do not populatea cdsAlnContainer before we removed host-reads!
            # We do not want to do unneccessary job!
        
        pass # Should be implemented
    
    # Determines reads which belong to the host and identifies it.
    # Removes host reads from the ReadContainer - they are not needed in the
    # following phases.
    #
    # Precondition:     ReadContainer is populated
    # Postcondition:    Host reads are removed from ReadContainer
    #
    # @return   Host, not defined yet how - just string with name, or object
    #                                       with some additional data?
    #
    def determineHost():

        # Implementation idea: 
        #
        # GI (genome index) of reads that belong to host directs us to
        # eukaryotes - as host is guarranteed to be an animal (by Innocentive),
        # this is the right way to determine host reads.
        # 
        # Pseudocode:
        #
        # for read in allReads:
        #   if (read.GI) is Eukaryote - not sure how to do this step, some
        #                               database should be queried with this read.GI
        #
        #       remember which Eukaryote - so we can determine host
        #
        #       remove read from readContainer
        #
    
        pass
        
    # Determines proteins (products) which are produced from CDSs of non-host reads.
    # 
    # Precondition: CdsAlnContainer is populated (or this is done in this method as
    #               a first thing)
    #   
    # @return   List of products (objects, strings or sth)
    #
    def determineProducts();

        # Implementation idea:
        #
        # Firstly, for each CDSAln is calculated its score (e.g. coverage)
        # Then, the following procedure is repeated:
        #
        #   REPEAT:
        #       bestCDS = getBestCDS()
        #       updateCDSs(bestCDS)
        #
        #   UNTIL all reads are "used" - each is assigned to one CDS

        pass

    # Gets currenly best CDS from CdsAlnContainer
    #
    def getBestCDS():
        pass

    # Updates all other CDSs after the best CDS is acquired:
    #   Remove reads from bestCDS from all other CDSs
    #   Update value (e.g coverage) for each CDS
    #
    def updateCDSs(bestCDS):
        pass

    # Removes reads from bestCDS from all other CdsAlns
    #
    def removeReadsFromAll(bestCDS):
        pass

