from data.containers.load   import initialize_containers
from ncbi.db.access         import DbQuery
from ncbi.db.taxonomy.tree  import TaxTree
from formats.xml_output     import *
from collections            import defaultdict


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
        
        # Populate readContainer

        # Do not populatea cdsAlnContainer before we removed host-reads!
            # We do not want to do unneccessary job!
        
        pass # Should be implemented

    # Here should go some User Interface methods like getXML(), solve() and similar

    def generateSolutionXML(self, alignment_file):
        ''' Main UI method.
            Generates XML file containing solution.
        '''
        # Initialize containers
        (read_container, record_container, cds_aln_container) = initialize_containers()
        # Create database access
        db_access = DbQuery()

        # Populate read container - NOT NOW NEEDED
        read_container.populate_from_aln_file (alignment_file)

        # Determine host - updates read container (remove/mark host alignments etc.) - DOES NOT
        # EXIST YET
        (host_taxid, host_read_cnt) = self.determine_host(read_container)

        # Populate CDS container 
        cds_aln_container.populate(read_container)

        # Map each read to one CDS (greedy)
        self.read2cds_solver.map_reads_2_cdss(cds_aln_container)

        # Determine species
        taxid2cdss = self.taxonomy_solver.map_cdss_2_species (db_access, read_container, cds_aln_container)

        # Generate XML file
        self.generateXML (host_taxid, host_read_cnt, taxid2cdss, cds_aln_container, db_access)

        print "Proba 0: funkcija generateXML prosla!"

        pass

    def generateXML (self, host_taxid, host_read_cnt, taxid2cdss, cds_aln_container,  db_access):

        tax_tree     = TaxTree()

        #-------------------------------DATASET-------------------------------#
        dataset = Dataset("Example2.fq", "Homo2", "sapiens", "human2", "9696", 
                  "eukaryota, ...; Homo", "Whole Blood2", "DNA", "single-end", "Roche 454")
        all_organisms = []

        #-------------------------------- HOST -------------------------------#
        host_name    = db_access.get_organism_name(host_taxid)
        host_lineage = tax_tree.get_taxonomy_lineage(host_taxid, db_access)
        (genus, species) = host_name.split()

        host = Organism (host_read_cnt, 0., str(host_taxid), host_lineage, host_name,
                 genus, species, [], [], [], is_host=True)
        all_organisms.append(host)

        #--------------------------- ORGANISMS ------------------------------#
        for (taxid, cdss) in taxid2cdss.items():
            organism_name    = db_access.get_organism_name (taxid)
            organism_lineage = tax_tree.get_taxonomy_lineage (taxid, db_access)
            org_name_details = organism_name.split()
            organism_count   = 0
            organism_reads   = []
            organism_genes   = []

            for cds_aln in cdss:
                # Increment organism count
                organism_count += cds_aln.get_active_alignment_cnt()
                # Find all reads mapped to organism
                for (read_id, cds_aln_subloc) in cds_aln.aligned_regions:
                    if cds_aln_subloc.active:
                        organism_reads.append (Read(read_id))
                # Append genes (protein_id, locus_tag, product, name)
                cds = cds_aln.cds
                organism_genes.append (Gene(cds.protein_id, cds.locus_tag, cds.product, cds.gene))

            organism = Organism (organism_count, 0., taxid, organism_lineage, organism_name,
                 org_name_details[0], org_name_details[1], organism_genes, [], organism_reads, is_host=False)
            all_organisms.append(organism)




        xml = XMLOutput(dataset, all_organisms) 
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

