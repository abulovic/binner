
class Solver (object):

    """ Solver uses other components (determineHost,
    Read2CDSSolver, TaxonomySolver) to solve whole problem.
    """

    def __init__ (self, read_container, cds_aln_container,
                  determine_host, read2cds_solver, taxonomy_solver):
        """
        @param (ReadContainer)      read_container Singleton instance
        @param (CdsAlnContainer)    cds_aln_container Singleton instance
        @param (function)           determine_host (to be specified yet)
        @param (Read2CDSSolver)     read2cds_solver
        @param (TaxonomySolver)     taxonomy_solver
        """
        self.read_container = read_container
        self.cds_aln_container = cds_aln_container
        self.determine_host = determine_host
        self.read2cds_solver = read2cds_solver
        self.taxonomy_solver = taxonomy_solver
        
        # Populate readContainer

        # Do not populatea cdsAlnContainer before we removed host-reads!
            # We do not want to do unneccessary job!
        
        pass # Should be implemented

    # Here should go some User Interface methods like getXML(), solve() and similar

    def generateSolutionXML(self):
        ''' Main UI method.
            Generates XML file containing solution.
        '''

        # Populate read container - NOT NOW NEEDED

        # Determine host - updates read container (remove/mark host alignments etc.) - DOES NOT
        # EXIST YET

        # Populate CDS container 
        self.cds_aln_container.populate(self.read_container)

        # Map each read to one CDS (greedy)
        self.read2cds_solver.map_reads_2_cdss(self.cds_aln_container)

        # Determine species

        # Generate XML file

        print "Proba 0: funkcija generateXML prosla!"

        pass

    def cds_to_species(cds):
        """ Map given cds to the species it belongs to.

            Each cds has the record_id of record it belongs to, and each record
            has gi which leads us to taxid (ncbitax database). 
            By knowing taxid we can easily determine species by looking into
            ncbitax database.
            
            Conclusion procedure:
                CDS -> record_id -> RECORD -> gi -> taxid -> 
                

            @param (cds)cds     input CDS
            @return (string)    the species to which given cds belongs to.


        """

    # -------------------------------------------- The following code will not be here ------------------------------------------ #
    
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
    def determineProducts():

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

