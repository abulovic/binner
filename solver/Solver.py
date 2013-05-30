from collections            import defaultdict

from data.containers.read   import ReadContainer
from data.containers.record import RecordContainer
from data.containers.cdsaln import CdsAlnContainer

from ncbi.db.access         import DbQuery
from ncbi.taxonomy.tree     import TaxTree

from statistics.SolverStatistics import SolverStatistics

from formats.xml_output     import *
import logging

class Solver (object):

    """ Solver uses other components (determineHost,
    Read2CDSSolver, TaxonomySolver) to solve whole problem.
    """

    def __init__ (self, determine_host, read2cds_solver, taxonomy_solver):
        """
        @param (function)           determine_host (to be specified yet)
        @param (Read2CDSSolver)     read2cds_solver
        @param (TaxonomySolver)     taxonomy_solver
        """
        self.determine_host = determine_host
        self.read2cds_solver = read2cds_solver
        self.taxonomy_solver = taxonomy_solver
        self.log = logging.getLogger(__name__)
        # Populate readContainer

        # Do not populatea cdsAlnContainer before we removed host-reads!
            # We do not want to do unneccessary job!
        
        pass # Should be implemented

    # Here should go some User Interface methods like getXML(), solve() and similar

    def generateSolutionXML(self, alignment_file, dataset_xml_file, output_solution_filename):
        ''' Main UI method.
            Generates XML file containing solution.
        '''
        # Create holder for statistical data
        stats = SolverStatistics()

        # Initialize containers
        read_container = ReadContainer()
        record_container = RecordContainer()
        cds_aln_container = CdsAlnContainer()
        # create taxonomy tree
        tax_tree = TaxTree()
        # Create database access
        db_access = DbQuery()
        record_container.set_db_access(db_access)
        # Populate read container - NOT NOW NEEDED
        read_container.populate_from_aln_file (alignment_file)
        self.log.info("Read container populated!")
        # Extract all records from database
        record_container.populate(read_container)
        self.log.info("Record container populated!")
        # find intersecting cdss for read alignments
        read_container.populate_cdss(record_container)
        self.log.info("read populate cdss over")
        read_cnt = len(read_container.fetch_all_reads(format=list))

        # for logging data BEGIN PHASE 1
        # taxon ids - very slow!!!
        #for (ncul_acc, record) in record_container.fetch_all_records(format=list):
        #    if record is not None:
        #        print record.sources[0].db_xref
        # for logging data END

        stats.collectPhaseData(1, record_container, read_container)

        print "determining host"
        # Determine host - updates read container (remove/mark host alignments etc.) - DOES NOT
        # EXIST YET
        (host_taxid, host_read_cnt, read_container) = self.determine_host(read_container)
        self.log.info("host_taxid:%s host_read_cnt:%s", str(host_taxid), str(host_read_cnt))
        if host_taxid:
            self.log.info("Host identified: %d!", (int(host_taxid)))

        # Populate CDS container 
        cds_aln_container.populate(read_container)
        self.log.info("Cds Aln Container populated!")

        stats.collectPhaseData(2, record_container, read_container, cds_aln_container)

        # Map each read to one CDS (greedy)
        self.read2cds_solver.map_reads_2_cdss(cds_aln_container)
        self.log.info("Reads mapped to CDSS.")

        stats.collectPhaseData(3, record_container, read_container, cds_aln_container)

        # Determine species
        taxid2cdss = self.taxonomy_solver.map_cdss_2_species (db_access, tax_tree, read_container, cds_aln_container)
        self.log.info("Taxonomy determined.")

        stats.collectPhaseData(4, record_container, read_container, cds_aln_container)        
        
        # Generate XML file
        self.generateXML (host_taxid, host_read_cnt, read_cnt, taxid2cdss, cds_aln_container, db_access, tax_tree, dataset_xml_file, output_solution_filename)

        stats.collectPhaseData(5, record_container, read_container, cds_aln_container)
        
        self.log.info("Proba 0: funkcija generateXML prosla!")

        print stats
        # Write stats to files
        stats.writeToFiles()
        
        pass



    def generateXML (self, host_taxid, host_read_cnt, read_cnt, taxid2cdss, cds_aln_container,  db_access, tax_tree, dataset_xml_file, output_solution_filename):

#        tax_tree     = TaxTree()

        #-------------------------------DATASET-------------------------------#
        dataset = Dataset(dataset_xml_file)
        all_organisms = []

        #-------------------------------- HOST -------------------------------#
        host_relative_amount = float(host_read_cnt)/read_cnt
        host = Organism (host_read_cnt, host_relative_amount, None, None, "Host",
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





    def cds_to_species(cds):
        """ Map given cds to the species it belongs to.

            Each cds has the record_id of record it belongs to, and each record
            has gi which leads us to taxid (ncbitax database). 
            By knowing taxid we can easily determine species by looking into
            ncbitax database.
            
            Conclusion procedure:
                CDS -> record_id -> RECORD -> gi -> taxid -> 
                

            @param (cds)cds     input CDS
            @return (string)    the species to which given cds belongs to.


        """

    # -------------------------------------------- The following code will not be here ------------------------------------------ #
    
    # Determines reads which belong to the host and identifies it.
    # Removes host reads from the ReadContainer - they are not needed in the
    # following phases.
    #
    # Precondition:     ReadContainer is populated
    # Postcondition:    Host reads are removed from ReadContainer
    #
    # @return   Host, not defined yet how - just string with name, or object
    #                                       with some additional data?
    #
    def determineHost():

        # Implementation idea: 
        #
        # GI (genome index) of reads that belong to host directs us to
        # eukaryotes - as host is guarranteed to be an animal (by Innocentive),
        # this is the right way to determine host reads.
        # 
        # Pseudocode:
        #
        # for read in allReads:
        #   if (read.GI) is Eukaryote - not sure how to do this step, some
        #                               database should be queried with this read.GI
        #
        #       remember which Eukaryote - so we can determine host
        #
        #       remove read from readContainer
        #
    
        pass
        
    # Determines proteins (products) which are produced from CDSs of non-host reads.
    # 
    # Precondition: CdsAlnContainer is populated (or this is done in this method as
    #               a first thing)
    #   
    # @return   List of products (objects, strings or sth)
    #
    def determineProducts():

        # Implementation idea:
        #
        # Firstly, for each CDSAln is calculated its score (e.g. coverage)
        # Then, the following procedure is repeated:
        #
        #   REPEAT:
        #       bestCDS = getBestCDS()
        #       updateCDSs(bestCDS)
        #
        #   UNTIL all reads are "used" - each is assigned to one CDS

        pass

    # Gets currenly best CDS from CdsAlnContainer
    #
    def getBestCDS():
        pass

    # Updates all other CDSs after the best CDS is acquired:
    #   Remove reads from bestCDS from all other CDSs
    #   Update value (e.g coverage) for each CDS
    #
    def updateCDSs(bestCDS):
        pass

    # Removes reads from bestCDS from all other CdsAlns
    #
    def removeReadsFromAll(bestCDS):
        pass

