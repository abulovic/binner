# @author: Martin Sosic, sosic.martin@gmail.com

class Read2CDSSolver (object):
    """ Class that decides for each read to which CDS does it belong (to which CDS does it map).
    It operates on CdsAlnContainer -> it uses data from it and modifies it.
    Method map_reads_2_cdss() must be called first.
    """

    def __init__(self):
        """
        (CdsAlnContainer) _cds_aln_container It contains list of all CDSs. Solver operates upon it.
        """
        self._cds_aln_container = None


    # Should be overrided and called with super() at the beginning of overriding method.
    def map_reads_2_cdss(self, cds_aln_container):
        """ Main method of solver: it decides for each read to which cds does it belong(map).
        When method is finished CDS alignment container will be modified in such way that 
        there will not be two CDSs that have same read assigned (each read will be assigned to exactly one CDS).
        Read is considered to be assigned to CDS if it is activated (attribute active) in cds alignment of that CDS.
        @param (CdsAlnContainer) cdsAlnContainer Reference to container is stored in object to be used for possible updating.
        """
        self._cds_aln_container = cds_aln_container

    # Should be overrided and called with super() at the beginning of overriding method.
    def remap_reads_from_cds(self, cds_aln): 
        """ Called after map_reads_2_cdss. It takes reads from given cds and maps them to other cdss.
        No reads remain mapped to given cds.
        Works upon cds alignment container that was given in map_reads_2_cdss().
        @param (CdsAlignment) cds_aln
        """
        if (self._cds_aln_container == None):
            raise Exception ("Cds alignment container was not specified! Have you executed map_reads_2_cdss?")


    def _activate_read(self, aln_reg):
        """ Activates read.
        @param (CdsAlnSublocation) aln_reg Representation of read with accordance to specific cds.
        """
        aln_reg.active = True

    def _deactivate_read(self, aln_reg):
        """ Deactivates read.
        @param (CdsAlnSublocation) aln_reg Representation of read with accordance to specific cds.
        """
        aln_reg.active = False

    def _is_read_active(self, aln_reg):
        """ Returns true if read is active, otherwise false.
        @param (CdsAlnSublocation) aln_reg Representation of read with accordance to specific cds.
        """
        return aln_reg.active
