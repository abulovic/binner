import sys, os
sys.path.append(os.getcwd())

from solutiondata           import *
from ncbi.db.access         import DbQuery

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
        self.organism_comparison = None

        # ----------------------------- Read stats for every organism ----------------------------- #

        db_query = DbQuery()
        # For every organism
            # Store total number of reported reads
            # For every read reported in solution XML:
                # If we potentially reported it -> counter ++

        organism_read_stats = {};
        for organism in solution_data:

            total_reported_reads_in_organism = len(organism.reads)
            reads_we_found = 0

            for read_id in organism.reads:
                gis     = [ read_aln.genome_index for read_aln in read_cont.read_repository[read_id].alignment_locations ]
                tax_ids = db_query.get_taxids(gis, list)

                if organism.taxon_id in tax_ids:
                    reads_we_found += 1

            organism_read_stats[organism.taxon_id] =  [reads_we_found, total_reported_reads_in_organism]

        self.read_comparison = organism_read_stats

        # ---------------------------------------------------------------------------------------- #


        self.cds_comparison = ComparisonData.cds_comparison(solution_data, cds_aln_cont, read_cont)

    @classmethod
    def cds_comparison(cls, solution_data, cds_aln_cont=None, read_cont=None):
        """ Does comparison between genes from solution and active cds from Solver.
        For each organism from solution we report:
         (1) number of genes from solution
         (2) number of genes from solution that have at least one corresponding
         active cds in Solver and thus could become part of our solution.
         @param (ReadContainer) read_cont  Populate_cdss() must have been called.
         @param ([Organism]) solution_data
         @return (dict) where key is taxon_id of organism and value
                        is list [(1), (2)].
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

        # This is what we will calculate.
        # Key is taxon_id, value is [number of cds in solution,
        # num of cds in solution that are active in container]
        org_stats = dict() 
        for org in solution_data:
            org_stats[org.taxon_id] = [len(org.genes), 0]

        #---------------------- Fetch our cdss ------------------------#
        # Fetch our cdss (from cds_aln_cont if available, if not
        # then from read_cont).
        cdss = []
        # Fetch active cdss from cds aln container.
        if (cds_aln_cont is not None):
            for cds_aln in cds_aln_cont.cds_repository.values():
                if cds_aln.is_active():
                    cdss.append(cds_aln.cds)
        # Or fetch all cdss from read container.
        elif (read_cont is not None):
            for read in read_cont.read_repository.values():
                for read_aln in read.alignment_locations:
                    for cds_loc in read_aln.aligned_cdss:
                        cdss.append(cds_loc[0])
        #--------------------------------------------------------------#
                        
        # Count for each organism our cdss 
        # that are also contained in solution_data
        genes_found = set()
        for cds in cdss:
            taxon_id, gene = None, None
            # find gene for which cds.product == gene.product
            #                     or cds.gene == gene.name
            if cds.product in gene_product2org:
                taxon_id, gene = gene_product2org[cds.product]
            if cds.gene    in gene_name2org:
                taxon_id, gene = gene_name2org[cds.gene]
            if not (taxon_id is None):
                # Check if gene was already matched - it should never happen
                if gene in genes_found:
                    #print "WARNING: In solution comparison: CDS was matched to already matched gene."
                    pass
                else:
                    genes_found.add(gene)
                    org_stats[taxon_id][1] += 1
                #print cds_aln.cds.product, cds_aln.cds.gene, cds_aln.cds.protein_id, cds_aln
        return org_stats

        
    # Not used anywhere
    @classmethod
    def cds_equals_gene(cls, cds, gene):
        """
        @param (Cds) cds
        @param (Gene) gene
        @return True if cds equals gene, False otherwise.
        """
        return cds.product == gene.product or cds.gene == gene.name
        
    def shortStr(self):
        overlap, total = 0, 0
        for o, t in self.cds_comparison.values():
            overlap += o
            total += t
        ret = "Cds overlap: " + str(overlap) + "/" + str(total) + "\n"

        overlap, total = 0, 0
        for o, t in self.read_comparison.values():
            overlap += o
            total += t
        ret += "Read overlap: " + str(overlap) + "/" + str(total) + "\n"

        return ret
                
            
    
