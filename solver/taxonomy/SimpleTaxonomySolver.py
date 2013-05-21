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
                cds = cds_aln.cds
                record = cds.record
                # try to fetch taxid from record data. If that fails,
                # find taxid through GI from record
                try:
                    gi = record.gi
                except AttributeError:
                    print "Cannot find GI for {0}. (SimpleTaxonomySolver)".format(cds_aln)
                    continue
                try:
                    [taxid] = db_access.get_taxids ([int(gi)], format=list)
                except TypeError:
                    # could not find GI in the database:
                    print "Cannot find taxid for GI {0}. (SimpleTaxonomySolver)".format(gi)
                    continue
		except ValueError:
		    print "Cannot find taxid for GI {0}. (SimpleTaxonomySolver)".format(gi)
                    continue

                assigned_taxids[taxid].append(cds_aln)
                
        return assigned_taxids


