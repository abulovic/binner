import logging
log = logging.getLogger(__name__)

class TaxonomySolver (object):
    """ Class that uses taxonomy tree to determine species.
    It interacts with Read2CDSSolver in order to update read to cds mapping
    after deciding that certain species are to be disregarded.
    """
    pass

    def stats_tax_ids (self, db_access, read_container, cds_aln_container):
        
        cds_alns = cds_aln_container.fetch_all_cds_alns()
        tax_ids = set([])
        
        for cds_aln in cds_alns:
            if cds_aln.is_active():
                taxid = self._get_taxid_from_gi (cds_aln, db_access)
                if not taxid:
                    continue
                tax_ids.add(taxid)
         
        return tax_ids

    def map_cdss_2_species (self, db_access, tax_tree, read_container, cds_aln_container):
        '''
        Maps CDS to species. 
        CDS can be mapped directly to the species it belongs to, 
        or it can be assigned to a higher-level taxonomical rank.
        CDS can also be disregarded if the species it belongs to
        isn't represented with enough CDSs.
        @param db_access         (DbQuery)
        @param tax_tree          (TaxTree)
        @param read_container    (ReadContainer)
        @param cds_aln_container (CdsAlnContainer)
        '''
        pass

    def _get_taxid_from_gi (self, cds_aln, db_access):
        tax_id = None
        try:
            tax_id = cds_aln.cds.taxon
        except AttributeError, e:
            # no taxon attribute, fallback to GI
            pass
        gi = cds_aln.cds.nucl_gi
        try:
            [tax_id] = db_access.get_taxids([gi], format=list)
        except ValueError, e:
            log.info ("TaxSolver: unable to fetch tax_id from gi = %d", gi)
        return tax_id
