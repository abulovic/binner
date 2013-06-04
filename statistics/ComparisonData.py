class ComparisonData (object):
    """ This class contains data comparison between final result and
        one of solver phases.
    """

    def __init__(self, solution_data, record_cont, read_cont, cds_aln_cont=None,
                 taxid2cdss=None):
        """ Takes solution data and data that represents current state of solver,
        compares them and stores comparison result in self.
        @param ([Organism]) solution_data  Contains solution data.
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        @param (dict) taxid2cdss  Result of TaxonomySolver
        """

        # Ovdje izracunati rezultate usporedbe i pospremiti u atribute.
        # One koji se ne mogu izracunati jer fale podaci postavi se na None.
        self.cds_comparison = cds_comparison(solution_data, cds_aln_cont)
        self.organism_comparison = None

    @classmethod
    def cds_comparison(solution_data, cds_aln_cont):
        """ 
        """
        gene2org = dict() # Key is protein_id, value is taxon_id
        for org in solution_data:
            for gene in org.genes:
                gene2org[protein_id] = org.taxon_id

        # This is what we will calculate.
        # Key is taxon_id, value is (number of cds in solution,
        # num of cds in solution that are active in container)
        org_stats = dict() 
        for org in solution_data:
            org_stats[org.taxon_id] = (len(org.genes), 0)

        # Count for each organism active cdss in container 
        # that are also contained in solution_data
        for cds_aln in cds_aln_cont.cds_repository.values():
            if cds_aln.is_active() and gene2org.has_key(cds_aln.cds.protein_id):
                taxon_id = gene2org[cds_aln.cds.protein_id]
                org_stats[taxon_id][1] += 1

        return org_stats
                
            
                
            
        
