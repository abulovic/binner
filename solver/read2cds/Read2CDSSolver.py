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
    def remove_cds_and_remap_reads(self, cds_aln): 
        """ Called after map_reads_2_cdss.
        It remaps active reads from given cds alignment to alternative cds alignments.
        After that it deletes given cds alignment from cds alignment container.
        Each read is activated in some alternative cds alignment (if there is one).
        If read has no alternative cds alignments then it will not be maped anywhere. 
        Works upon cds alignment container that was given in map_reads_2_cdss(),
        which will be modified.
        @param (CdsAlignment) cds_aln
        @return ({read_id:CdsAlignment}) Dictionary where key is read_id and value is
                                         cds alignment to which it maps. 
                                         If it does not map anywhere then value is None.
        """
        if (self._cds_aln_container == None):
            raise Exception ("Cds alignment container was not specified! Have you executed map_reads_2_cdss?")

    @staticmethod
    def test_cds_alignment_container_consistency(cds_aln_container):
        """ This function is intended to be used for testing purposes. 
        It should be run after execution of map_reads_2_cdss() or
        after execution of remove_cds_and_remap_reads in order to test
        cds alignment container for consistency.
        Cds alignment container is considered to be consistent (after execution
        of map_reads_2_cdss()) if each read is active in (mapped to) at most
        one cds alignment. Also, if cds alignment contains read (active or not),
        that cds must be element of read2cds for that read and vice versa.
        @param (CdsAlnContainer) cds_aln_container Container produced using map_reads_2_cdss().
        @return (boolean) True if test passed, False otherwise.
        """
        active_read_ids = set()
        for cds_aln in cds_aln_container.cds_repository.values():
            for aln_reg in cds_aln.aligned_regions.values():
                if aln_reg.active:
                    # Check if it is active in some other cds.
                    if aln_reg.read_id in active_read_ids: return False
                    else: active_read_ids.add(aln_reg.read_id)
                # Check if there is mapping in read2cds.
                if not(cds_aln in cds_aln_container.read2cds[aln_reg.read_id]):
                    return False
        # For each mapping in read2cds check if there is mapping in cds_repository.
        for (read_id, cds_alns) in cds_aln_container.read2cds.items():
            for cds_aln in cds_alns:
                try:
                    if not(read_id in cds_aln_container.cds_repository[cds_aln.cds].aligned_regions.keys()):
                        return False
                except KeyError:
                    return False

        return True

