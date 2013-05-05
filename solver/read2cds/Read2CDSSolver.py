class Read2CDSSolver (object):
    """ Class that decides for each read to which CDS does it belong (to which CDS does it map).
    It operates on CdsAlnContainer -> it uses data from it and modifies it.
    Method register_cds_aln_container(...) must be called first.
    """

    def __init__(self):
        """
        (CdsAlnContainer) _cds_aln_container It contains list of all CDSs. Solver operates upon it.
        """
        self._cds_aln_container = None

    def register_cds_aln_container(self, cds_aln_container):
        """ Register cds alignment container to work with.
        This method must be called before any other methods.
        @param (CdsAlnContainer) cdsAlnContainer Singleton instance.
        """ 
        self._cds_aln_container = cds_aln_container


    # Should be overrided and called with super() at the beginning of overriding method.
    def map_reads_2_cdss(self):
        """ Main method of solver: it decides for each read to which cds does it belong(map).
        When method is finished CDS alignment container will be modified in such way that 
        there will not be two CDSs that have same read assigned (each read will be assigned to exactly one CDS).
        """
        if (self._cds_aln_container == None):
            raise Exception("CDS alignment container not registered!")
            
    def remap_reads_from_cds(self, cds_aln): #Sto ona prima kao argument? Neki id cds-a ili sto?
        """ Called after map_reads_2_cdss. It takes reads from given cds and maps them to other cdss.
        No reads remain mapped to given cds.
        """
        # Should it throw an exception if map_reads_2_cdss has not been executed before?
        pass

    
    # Should be overrided -> Does this even need to be in base class?
    def _calcCoverage(self, cds_aln):
        """
        @param (CdsAlignment) cdsAlignment Calculates coverage of given cdsAlignment.
        """
        pass
