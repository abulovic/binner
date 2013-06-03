from TaxonomySolver import TaxonomySolver
from collections import defaultdict


class SimpleJoinTaxonomySolver (TaxonomySolver):
    '''
    If the organism rank is too low (not species, but assigned
    a specific sequencing ID), it is pushed up in the taxonomy tree
    to the first species node.
    '''
    
    def map_cdss_2_species (self, db_access, tax_tree, read_container, cds_aln_container):

        assigned_taxids = defaultdict(list)
        cds_alns = cds_aln_container.fetch_all_cds_alns()
        ref_taxids = {}

        for cds_aln in cds_alns:
            if cds_aln.is_active():
                
                # 1. fetch taxonomy ID
                taxid = self._get_taxid_from_gi (cds_aln, db_access)
                if not taxid:
                    continue
                # 2. determine tax ID to which this taxid maps
                if ref_taxids.has_key(taxid):
                    ref_taxid = ref_taxids[taxid]
                else:
                    ref_taxid = self.get_ref_taxid (taxid, db_access, tax_tree)
                    ref_taxids[taxid] = ref_taxid
                # 3. report this cds for referent taxid
                assigned_taxids[ref_taxid].append(cds_aln)
                
        return assigned_taxids

    def get_ref_taxid(self, taxid, db_access, tax_tree):
        organism_name = db_access.get_organism_name (taxid)
        if not organism_name:
            return taxid
        name_parts = organism_name.split()
        if len(name_parts) <= 2:
            return taxid

        ref_name = organism_name
        lineage = tax_tree.get_taxonomy_lineage(taxid, db_access)
        lineage.reverse()
        for tax_name in lineage:
            name_parts = tax_name.split()
            if len(name_parts) <= 2:
                ref_name = tax_name
                break
        taxid = db_access.get_organism_taxid (ref_name)
        return taxid
        
            
