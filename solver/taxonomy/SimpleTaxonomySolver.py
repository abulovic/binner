from TaxonomySolver import TaxonomySolver
from collections    import defaultdict

class SimpleTaxonomySolver (TaxonomySolver):
    '''
    A basic implementation of a taxonomy solver. For each CDS alignments,
    assigns the taxonomy ID the CDS belongs to.
    It does no filtering of the under-represented species.
    '''

    def map_cdss_2_species (self, db_access, tax_tree, read_container, cds_aln_container):
        '''
        Determines species for each CDS. 
        @param db_access (DbQuery) 
        @param read_container (ReadContainer)
        @param cds_aln_container (CdsAlnContainer)
        @return assigned_taxids (dict, key: taxid, value: cds list)
        '''
        assigned_taxids = defaultdict(list)
        cds_alns        = cds_aln_container.fetch_all_cds_alns()

        for cds_aln in cds_alns:
            if cds_aln.is_active():
                taxid = self._get_taxid_from_gi (cds_aln, db_access)
                if not taxid:
                    continue
                assigned_taxids[taxid].append(cds_aln)
        return assigned_taxids


