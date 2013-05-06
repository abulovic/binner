class TaxonomySolver (object):
    """ Class that uses taxonomy tree to determine species.
    It interacts with Read2CDSSolver in order to update read to cds mapping
    after deciding that certain species are to be disregarded.
    """
    pass

    def map_cdss_2_species (self, db_access, read_container, cds_aln_container):
        '''
        Maps CDS to species. 
        CDS can be mapped directly to the species it belongs to, 
        or it can be assigned to a higher-level taxonomical rank.
        CDS can also be disregarded if the species it belongs to
        isn't represented with enough CDSs.
        @param db_access         (DbQuery)
        @param read_container    (ReadContainer)
        @param cds_aln_container (CdsAlnContainer)
        '''
        pass


