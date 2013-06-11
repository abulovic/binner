import sys, os
sys.path.append(os.getcwd())
import logging

from solutiondata           import *
from ncbi.db.access         import DbQuery

log = logging.getLogger(__name__)

class ComparisonData (object):
    """ This class contains data comparison between final result and
        one of solver phases.
    """

    def __init__(self):
        """ Takes solution data and data that represents current state of solver,
        compares them and stores comparison result in self.
        @param ([Organism]) solution_data  Contains solution data.
        @param (RecordContainer) record_cont
        @param (ReadContainer) read_cont
        @param (CdsAlnContainer) cds_aln_cont
        @param (dict) taxid2cdss  Result of TaxonomySolver
        """

        self.taxid2cdss_comparison  = None
        self.cds_comparison         = None
        self.taxid2reads_comparison = None
        self.read_comparison        = None
        self.taxid_comparison       = None
        

    @classmethod
    def taxid2cdss_comparison(cls, solution_data, taxid2cdss):
        """ Does comparison of taxid2cdss mappings (final result of solver).
        @return (dict) Key: taxon_id (Which means each entry is one organism).
                       Value: [num_cds_in_solution, num_cds_that_we_reported,
                               overlap].
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
        # num of cds that we reported,
        # num of cds that we reported for that organism that are in solution]
        org_stats = dict() # contains data about union of organisms from our solution and correct solution
        for org in solution_data:
            if org.taxon_id in org_stats:
                org_stats[org.taxon_id][0] = len(org.genes)
            else:
                org_stats[org.taxon_id] = [len(org.genes), 0, 0]
        for taxon_id, cds_alns in taxid2cdss.items():
            if taxon_id in org_stats:
                org_stats[taxon_id][1] = len(cds_alns)
            else:
                org_stats[taxon_id] = [0, len(cds_alns), 0]


        for taxon_id, cdss in taxid2cdss.items():
            genes_found = set()
            for cds_aln in cds_alns:
                cds = cds_aln.cds
                gene_taxon_id, gene = None, None
                # find gene for which cds.product == gene.product
                #                     or cds.gene == gene.name
                if cds.product in gene_product2org:
                    gene_taxon_id, gene = gene_product2org[cds.product]
                if cds.gene    in gene_name2org:
                    gene_taxon_id, gene = gene_name2org[cds.gene]
                if gene_taxon_id == taxon_id:
                    if gene in genes_found:
                        log.info("In solution comparison: CDS was matched to already matched gene.")
                        pass
                    else:
                        genes_found.add(gene)
                        org_stats[taxon_id][2] += 1

        return org_stats
                
    @classmethod
    def read_comparison(cls, solution_data, read_cont):
        """
        """
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

            organism_read_stats[organism.taxon_id] =  [total_reported_reads_in_organism, reads_we_found]

        return organism_read_stats
            

    @classmethod
    def cds_comparison(cls, solution_data, cds_aln_cont=None, read_cont=None):
        """ Does comparison between genes from solution and active cds from Solver.
        read_cont is used only if cds_aln_cont is None.
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
        if cds_aln_cont is not None:
            for cds_aln in cds_aln_cont.cds_repository.values():
                if cds_aln.is_active():
                    cdss.append(cds_aln.cds)
        # Or fetch all cdss from read container.
        elif read_cont is not None:
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
            if taxon_id is not None:
                if gene in genes_found:
                    log.info("In solution comparison: CDS was matched to already matched gene.")
                    pass
                else:
                    genes_found.add(gene)
                    org_stats[taxon_id][1] += 1

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
        

    @classmethod
    def taxid2cdss_orgs_vs_orgs(cls, solution_data, solver_data):
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
        # num of cds that we reported,
        # num of cds that we totally correctly reported,
        # num of cds that we reported correctly but to wrong taxon_id,
        # num of cds that we reported wrong]
        org_stats = dict() # contains data about union of organisms from our solution and correct solution
        for org in solution_data:
            if org.taxon_id in org_stats:
                org_stats[org.taxon_id][0] = len(org.genes)
            else:
                org_stats[org.taxon_id] = [len(org.genes), 0, 0, 0, 0]
        for org in solver_data:
            if org.taxon_id in org_stats:
                org_stats[org.taxon_id][1] = len(org.genes)
            else:
                org_stats[org.taxon_id] = [0, len(org.genes), 0, 0, 0]

        for org in solver_data:
            taxon_id = org.taxon_id
            genes_found = set()
            for gene in org.genes:
                solution_taxon_id, solution_gene = None, None
                # find gene for which gene.product == gene.product
                #                     or gene.name == gene.name
                if gene.product in gene_product2org:
                    solution_taxon_id, solution_gene = gene_product2org[gene.product]
                if gene.name    in gene_name2org:
                    solution_taxon_id, solution_gene = gene_name2org[gene.name]
                if solution_taxon_id is not None:
                    if solution_gene in genes_found:
                        log.info("In solution comparison: CDS was matched to already matched gene.")
                        pass
                    else:
                        genes_found.add(solution_gene)
                        if solution_taxon_id == taxon_id:
                            org_stats[taxon_id][2] += 1
                        else:
                            org_stats[taxon_id][3] += 1
                else:
                    org_stats[taxon_id][4] += 1

        return org_stats


    @classmethod
    def taxid_orgs_vs_orgs(cls, solution_data, solver_data):
        """
        @return [num of taxids in solution,
                 num of taxids solver found,
                 num of taxids solver found correctly]
        """
        solution_taxon_ids = set()
        for org in solution_data:
            solution_taxon_ids.add(org.taxon_id)

        correct_taxon_ids = set()
        for org in solver_data:
            if org.taxon_id in solution_taxon_ids:
                correct_taxon_ids.add(org.taxon_id)

        return [len(solution_data), len(solver_data), len(correct_taxon_ids)]
                

    @classmethod
    def reads_orgs_vs_orgs(cls, solution_data, solver_data):
        """
        @return (dict) Key: taxon_id of organism.
                       Value: [num of reads from solution,
                               num of reads solver reported,
                               num of reads solver totally correctly reported,
                               num of reads solver correctly reported but missed organism,
                               num of reads solver reported wrong]
        """
        taxid2reads_comparison = dict()
        for org in solution_data:
            num_reads = 0 if org.reads is None else len(org.reads)
            taxid2reads_comparison[org.taxon_id] = [num_reads, 0, 0, 0, 0]
        for org in solver_data:
            num_reads = 0 if org.reads is None else len(org.reads)
            if org.taxon_id in taxid2reads_comparison:
                taxid2reads_comparison[org.taxon_id][1] = num_reads
            else:
                taxid2reads_comparison[org.taxon_id][1] = [0, num_reads, 0, 0, 0]

        solution_reads = dict()
        for org in solution_data:
            if org.reads is not None:
                for read_id in org.reads:
                    solution_reads[read_id] = org.taxon_id

        for org in solver_data:
            if org.reads is not None:
                for read_id in org.reads:
                    if read_id in solution_reads:
                        if org.taxon_id == solution_reads[read_id]:
                            taxid2reads_comparison[org.taxon_id][2] += 1
                        else:
                            taxid2reads_comparison[org.taxon_id][3] += 1
                    else:
                        taxid2reads_comparison[org.taxon_id][4] += 1
                        
        return taxid2reads_comparison


    @classmethod
    def solution_data_vs_solver_data(cls, solution_data, solver_data):
        cd = ComparisonData()
        
        cd.taxid2cdss_comparison = ComparisonData.taxid2cdss_orgs_vs_orgs(solution_data, solver_data)

        cd.taxid_comparison = ComparisonData.taxid_orgs_vs_orgs(solution_data, solver_data )

        cd.taxid2reads_comparison = ComparisonData.reads_orgs_vs_orgs(solution_data, solver_data)

        return cd


    @classmethod
    def solution_data_vs_solver(cls, solution_data, record_cont, read_cont, 
                                cds_aln_cont=None, taxid2cdss=None):
        cd = ComparisonData()

        cd.read_comparison = ComparisonData.read_comparison(solution_data, read_cont)
        cd.cds_comparison = ComparisonData.cds_comparison(solution_data, cds_aln_cont, read_cont)
        if taxid2cdss is not None:
            cd.taxid2cdss_comparison = ComparisonData.taxid2cdss_comparison(solution_data, taxid2cdss)

        return cd


    def shortStr(self):
        ret = ""
        if self.cds_comparison is not None:
            overlap, total = 0, 0
            for t, o in self.cds_comparison.values():
                overlap += o
                total += t
            ret += "Cdss (matched, total in solution): " + str(overlap) + "/" + str(total) + "\n"

        if self.read_comparison is not None:
            overlap, total = 0, 0
            for t, o in self.read_comparison.values():
                overlap += o
                total += t
            ret += "Reads (matched, total in solution): " + str(overlap) + "/" + str(total) + "\n"

        if self.taxid2reads_comparison is not None:
            ret += """taxid2reads:  taxid, 
                (# reads in solution,
                 # reads in solver output,
                 # reads from solver that have match in solution under same organism, 
                 # reads from solver that have match in solution under another organism,
                 # reads from solver that have no match in solution)\n"""
            for taxon_id, comp_data in self.taxid2reads_comparison.items():
                ret += "    " + str(taxon_id) + ":  " + str(comp_data) + "\n"

        if self.taxid2cdss_comparison is not None:
            ret += """taxid2cdss:  taxid, 
                (# cdss in solution,
                 # cdss in solver output,
                 # cdss from solver that have match in solution under same organism, 
                 # cdss from solver that have match in solution under another organism,
                 # cdss from solver that have no match in solution)\n"""
            for taxon_id, comp_data in self.taxid2cdss_comparison.items():
                ret += "    " + str(taxon_id) + ":  " + str(comp_data) + "\n"

        if self.taxid_comparison is not None:
            ret += "Organisms (# orgs in solution, # orgs in solver output, # orgs that are in both): " + str(self.taxid_comparison) + "\n"

        return ret
                
    def __str__(self):
        return self.shortStr()
            
    
