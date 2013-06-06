import sys, os
sys.path.append(os.getcwd())

from solutiondata import *

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
        self.cds_comparison = None
        self.organism_comparison = None

        if not (cds_aln_cont is None):
            self.cds_comparison = ComparisonData.cds_comparison(solution_data, cds_aln_cont)

    @classmethod
    def cds_comparison(cls, solution_data, cds_aln_cont):
        """ 
        """
        #---- Transform solution_data to be suitable for searching ----#
        # Dictionary where each entry represents one gene:
        # Key is gene.product, value is (org.taxon_id, gene)
        gene_product2org = dict() 
        # Dictionary where each entry represents one gene:
        # Key is gene.name, value is (org.taxon_id, gene)
        gene_name2org = dict()
        for org in solution_data:
            for gene in org.genes:
                gene_product2org[gene.product]  = (org.taxon_id, gene)
                gene_name2org[gene.name] = (org.taxon_id, gene)
        #--------------------------------------------------------------#

        print gene_product2org
        print gene_name2org

        # This is what we will calculate.
        # Key is taxon_id, value is [number of cds in solution,
        # num of cds in solution that are active in container]
        org_stats = dict() 
        for org in solution_data:
            org_stats[org.taxon_id] = [len(org.genes), 0]


        # Count for each organism active cdss in container 
        # that are also contained in solution_data
        genes_found = set()
        for cds_aln in cds_aln_cont.cds_repository.values():
            if cds_aln.is_active():
                taxon_id, gene = None, None
                # find gene for which cds.product == gene.product
                #                     or cds.gene == gene.name
                if cds_aln.cds.product in gene_product2org:
                    taxon_id, gene = gene_product2org[cds_aln.cds.product]
                if cds_aln.cds.gene    in gene_name2org:
                    taxon_id, gene = gene_name2org[cds_aln.cds.gene]
                if not (taxon_id is None):
                    org_stats[taxon_id][1] += 1
                    # Check if gene was already matched - it should never happen
                    if gene in genes_found:
                        print "WARNING: In solution comparison: CDS was matched to already matched gene."
                    else:
                        genes_found.add(gene)
                    print cds_aln.cds.product, cds_aln.cds.gene, cds_aln

        # TODO: assert that same gene is not twice counted.

 # TODO: take read container as argument, and if cds cont is not given,
 #       use read container to calculate result
                
        return org_stats
        
    @classmethod
    def cds_equals_gene(cls, cds, gene):
        """
        @param (Cds) cds
        @param (Gene) gene
        @return True if cds equals gene, False otherwise.
        """
        return cds.product == gene.product or cds.gene == gene.name
        
        
                
            
        
