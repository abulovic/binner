from collections            import defaultdict

from data.containers.cdsaln import CdsAlnContainer

from ncbi.db.access         import DbQuery
from ncbi.taxonomy.tree     import TaxTree

from statistics.SolverStatistics import SolverStatistics

from formats.xml_output     import *
import logging
import time

from statistics.ComparisonData import ComparisonData
from statistics.solutiondata import loadOrganismData

class Solver (object):

    """ Solver uses other components (determineHost,
    Read2CDSSolver, TaxonomySolver) to solve whole problem.
    """

    def __init__ (self, host_determinator, read2cds_solver, taxonomy_solver):
        """
        @param (HostDeterminator)   Determines host in reads
        @param (Read2CDSSolver)     read2cds_solver
        @param (TaxonomySolver)     taxonomy_solver
        """
        self.host_determinator = host_determinator
        self.read2cds_solver = read2cds_solver
        self.taxonomy_solver = taxonomy_solver
        self.log = logging.getLogger(__name__)
        # Populate readContainer

        # Do not populatea cdsAlnContainer before we removed host-reads!
            # We do not want to do unneccessary job!
        
        pass # Should be implemented

    # Here should go some User Interface methods like getXML(), solve() and similar

    def generateSolutionXML(self, read_container, record_container,
                            dataset_xml_file, output_solution_filename,
                            stats_dir=None, solution_file=None):
        ''' Main UI method.
            Generates XML file containing solution.
            @param (ReadContainer) read_container Container with all the reads
            @param (RecordContainer) record_container Container with all the 
                records that will be used in the processing
            @param (String) dataset_xml_file  Filepath to dataset xml file
            @param (String) output_solution_filename  Filepath where xml output is stored.
            @param (String) stats_dir  Path to directory where statistics and comparison with solution
                                       will be stored.
                                       Path must be specified without / at the end.
                                       If directory does not exist, it will be created.
                                       If None, statistics are not stored.
            @param (String) solution_file  Path to file containing solution xml.
                                           If given, all phases will be compared to solution.
        '''
        # Create holder for statistical data
        stats = SolverStatistics()

        # load solution file
        if (solution_file is not None):
            solution_data = loadOrganismData(solution_file)

        # Initialize containers
        cds_aln_container = CdsAlnContainer()
        # create taxonomy tree
        tax_tree = TaxTree()
        # Create database access
        db_access = DbQuery()

        # --------------------------- #
        start = time.time()

        # find intersecting cdss for read alignments
        read_container.populate_cdss(record_container)
        self.log.info("read populate cdss over")

        end = time.time()
        elapsed_time = end - start
        print ("Populate cdss - \t\telapsed time: %.2f" % elapsed_time)

        # --------------------------- #

        read_cnt = len(read_container.fetch_all_reads(format=list))

        # for logging data BEGIN PHASE 1
        # taxon ids - very slow!!!
        #for (ncul_acc, record) in record_container.fetch_all_records(format=list):
        #    if record is not None:
        #        print record.sources[0].db_xref
        # for logging data END

        stats.collectPhaseData(1, record_container, read_container)

        if (solution_file is not None):
            compData = ComparisonData(solution_data, record_container, read_container)
            print compData.cds_comparison


        # --------------------------- #
        start = time.time()

        # Determine host - updates read container (remove/mark host alignments etc.) - DOES NOT
        # EXIST YET
        (host_taxid, host_read_count) = self.host_determinator.determine_host(read_container)
        self.log.info("host_taxid:%s host_read_count:%s", str(host_taxid), str(host_read_count))
        if host_taxid:
            self.log.info("Host identified: %d!", (int(host_taxid)))

        end = time.time()
        elapsed_time = end - start
        print ("Determine host - \t\telapsed time: %.2f" % elapsed_time)

        # --------------------------- #
        start = time.time()

        # Populate CDS container 
        cds_aln_container.populate(read_container.fetch_all_reads())
        self.log.info("Cds Aln Container populated!")

        end = time.time()
        elapsed_time = end - start
        print ("Populate CDS container - \telapsed time: %.2f" % elapsed_time)

        # --------------------------- #

        stats.collectPhaseData(2, record_container, read_container, cds_aln_container)

        if (solution_file is not None):
            compData = ComparisonData(solution_data, record_container, read_container, cds_aln_container)
            print compData.cds_comparison

        # --------------------------- #
        start = time.time()

        # Map each read to one CDS (greedy)
        self.read2cds_solver.map_reads_2_cdss(cds_aln_container)
        self.log.info("Reads mapped to CDSS.")

        end = time.time()
        elapsed_time = end - start
        print ("Greedy - \t\t\telapsed time: %.2f" % elapsed_time)

        # --------------------------- #

        stats.collectPhaseData(3, record_container, read_container, cds_aln_container)

        # --------------------------- #
        start = time.time()

        # Determine species
        taxid2cdss = self.taxonomy_solver.map_cdss_2_species (db_access, tax_tree, read_container, cds_aln_container)
        self.log.info("Taxonomy determined.")

        end = time.time()
        elapsed_time = end - start
        print ("Determine species - \t\telapsed time: %.2f" % elapsed_time)
        # --------------------------- #

        stats.collectPhaseData(4, record_container, read_container, cds_aln_container, taxid2cdss)        
        
        # --------------------------- #
        start = time.time()

        # Generate XML file
        self.generateXML (host_taxid, host_read_count, read_cnt, taxid2cdss, cds_aln_container, db_access, tax_tree, dataset_xml_file, output_solution_filename)

        end = time.time()
        elapsed_time = end - start
        print ("Generate XML file - \t\telapsed time: %.2f" % elapsed_time)

        # --------------------------- #

        stats.collectPhaseData(5, record_container, read_container, cds_aln_container)
        
        self.log.info("Proba 0: funkcija generateXML prosla!")

        print stats
        # --------------------------- #
        if (stats_dir is not None):
            start = time.time()

            # Write stats to files
            stats.writeToFiles(stats_dir)

            end = time.time()
            elapsed_time = end - start
            print ("Write stats to file - \t\telapsed time: %.2f" % elapsed_time)
        # --------------------------- #

        pass



    def generateXML (self, host_taxid, host_read_count, read_cnt, taxid2cdss, cds_aln_container,  db_access, tax_tree, dataset_xml_file, output_solution_filename):

#        tax_tree     = TaxTree()

        #-------------------------------DATASET-------------------------------#
        dataset = Dataset(dataset_xml_file)
        all_organisms = []

        #-------------------------------- HOST -------------------------------#
        host_relative_amount = float(host_read_count)/read_cnt
        host = Organism (host_read_count, host_relative_amount, None, None, "Host",
                 None, None, [], [], [], is_host=True)
        all_organisms.append(host)

        #--------------------------- ORGANISMS ------------------------------#
        for (taxid, cdss) in taxid2cdss.items():
            organism_name    = db_access.get_organism_name (taxid)
            if not organism_name:
                self.log.error("Unable to find name for taxid %d", taxid)
                organism_name = ""
                organism_lineage = ""
                org_species = ""
                org_genus = ""
                org_strain = ""
            else:
                organism_lineage = tax_tree.get_taxonomy_lineage (taxid, db_access)
                org_name_details = organism_name.split()
                org_species = org_name_details[0]
                if (len(org_name_details) > 1):
                    org_genus = org_name_details[1]
                else: 
                    org_genus = ""
                if (len(org_name_details) > 2):
                    org_strain = org_name_details[2:]
                else:
                    org_strain = ""

            organism_count   = 0
            organism_reads   = []
            organism_genes   = []

            for cds_aln in cdss:
                # Increment organism count
                organism_count += cds_aln.get_active_alignment_cnt()
                # Find all reads mapped to organism
                for (read_id, cds_aln_subloc) in cds_aln.aligned_regions.items():
                    if cds_aln_subloc.active:
                        organism_reads.append (Read(read_id))
                # Append genes (protein_id, locus_tag, product, name)
                cds = cds_aln.cds
                organism_genes.append (Gene(cds.protein_id, cds.locus_tag, cds.product, cds.protein_id, cds.gene))
	    
            org_relative_cnt = float(organism_count)/read_cnt
            organism = Organism (organism_count, org_relative_cnt, taxid, "; ".join(organism_lineage), organism_name,
                 org_species, org_genus, organism_genes, [], organism_reads, is_host=False)
            all_organisms.append(organism)




        xml = XMLOutput(dataset, all_organisms, output_solution_filename) 
        xml.xml_output();


