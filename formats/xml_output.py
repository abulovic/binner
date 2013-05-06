import sys, os
sys.path.append(os.getcwd())

from utils.autoassign import autoassign

class Dataset(object):

    @autoassign
    def __init__(self, name, host_genus, host_species, common_name, taxon_id, 
                 taxonomy, sample_source, sample_type, seq_method, sequencer):
        pass

class Gene(object):

    @autoassign
    def __init__(self, protein_id, locus_tag, product, name)
        pass 

class Organism(object):

    @autoassign
    def __init__(self, amount_count, amount_relative, taxon_id, taxonomy, name,
                 genus, species, genes, variants, reads, is_host=False):
        pass

class XMLOutput(object):

    def __init__(self, dataset, organisms):
        self.dataset = dataset
        self.organisms = organisms
        #itd. tu dodati koji sve ce vec ici, ne znam kako cemo tocno ove readove i organizme koji su iterativni, to vidjet s ostalima, mozda jos jednu strukturu dodat
        #potrebno je jos ove sve instance varijable spojiti u funkcijama da dobijemo odgovorajuci ispis

    def dataset_details_output(self, level):

        tab = " " * level * 2
        dataSetName = self.dataset.name
        hostGenus = self.dataset.host_genus
        hostSpecies = self.dataset.host_species
        commonName = self.dataset.common_name
        taxon_id = self.dataset.taxon_id
        taxonomy = self.dataset.taxonomy
        sampleSource = self.dataset.sample_source
        sampleType = self.dataset.sample_type
        seq_method = self.dataset.seq_method
        sequencer = self.dataset.sequencer

        print(tab + "<datasetName>" + dataSetName + "</datasetName>")
        print(tab + "<hostGenus>" + hostGenus + "</hostGenus>")
        print(tab + "<hostSpecies>" + hostSpecies + "</hostSpecies>")
        print(tab + "<commonName>" + commonName + "</commonName>")
        print(tab + "<taxonomy taxon_id=\"" + taxon_id  + "\">" + taxonomy + "</taxonomy>")
        print(tab + "<sampleSource>" + sampleSource + "</samleSource>")
        print(tab + "<sampleType>" + sampleType + "</sampleType>")
        print(tab + "<sequencer method=\"" + seq_method + "\">" + sequencer + "</sequencer>")

    def dataset_output(self, level):
        
        tab = " " * level * 2

        print(tab + "<dataset>")
        self.dataset_details_output(level+1)
        print(tab + "</dataset>")

    def gene_output(self, level):

        tab = " " * level * 2
        protein_id = "AAS638912.1"
        locus_tag = "YP_3766"
        product = "carbohidrati neke vrste"
        gene = "xy567"

        print(tab + "<gene protein_id=\"" + protein_id + "\" locus_tag=\"" + locus_tag + "\" product=\"" + product + "\">" + gene + "</gene>" )

    def variant_details(self, level):

        tab = " " * level * 2
        ref_name = "CAB78909.1"
        ref_start = "31"
        ref_seq = "-"
        variant = "A"
        offset = "28"
        genome_sequence = "ACTGATTTTTGGGGATAGTAGATGATGATCCAGTGATAG"

        print(tab + "<variant ref_name=\"" + ref_name + "\" ref_start=\"" + ref_start + "\" ref_seq=\"" + ref_seq + "\">" + variant + "</variant>")
        print(tab + "<context offset=\"" + offset + "\">" + genome_sequence + "</context>")

    def variant_output(self, level):

        tab = " " * level * 2

        print(tab + "<sequenceDifference>")
        self.variant_details(level+1)
        print(tab + "</sequenceDifference>")

    def sequence_output(self, level):

        tab = " " * level * 2
        sequence = "HT8943589J"

        print(tab + "<sequence>" + sequence + "</sequence>")

    def organism_details_output(self, level, organism, is_host=False):

        tab = " " * level * 2
        count = organism.amount_count
        rel_amount = organism.amount_relative
        taxon_id = organism.taxon_id
        taxonomy = organism.taxonomy
        organism_name = organism.name

        print(tab + "<relativeAmount count=\">" + count + "\">" + rel_amount + "</relativeAmount>")
        print(tab + "<taxonomy taxon_id=\"" + taxon_id  + "\">" + taxonomy + "</taxonomy>")
        print(tab + "<organsimName>" + organism_name + "</organismName>")

        if is_host:
            return

        genus = organism.genus
        species = organism.species

        print(tab + "<genus>" + genus + "</genus>")
        print(tab + "<species>" + species + "</species>")

        print(tab + "<genes>")
        # za svaki gen ispis ga, for petlja treba biti
        genes = organism.genes
        self.gene_output(level+1)
        print(tab + "<genes>")

        print(tab + "<variants>")
        # za svaku varijantu ispis, for petlja treba bit
        variants = organism.variants
        self.variant_output(level+1)
        print(tab + "</variants>")

        print(tab + "<reads>")
        reads = organism.reads
        self.sequence_output(level + 1)
        print(tab + "</reads>")

    def organism_output(self, level):

        tab = " " * level * 2

        for organism in self.organisms:
            print(tab + "<organism>")
            self.organism_details_output(level+1, organism)
            print(tab + "</organism>")

        '''
        print(tab + "<organism>")
        self.organism_details_output(level+1, True)
        print(tab + "</organism>")

        print(tab + "<organism>")
        # ovdje sad idu paraziti, znaci for petlja
        # za svaki parazit ispisi njegov xml
        self.organism_details_output(level+1)
        print(tab + "</organism>")
        '''

    def organisms_output(self, level):

        tab = " " * level * 2

        print(tab + "<organisms>")
        self.organism_output(level+1)
        print(tab + "</organisms>")

    def xml_output(self, level):

        print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
        print("<organismsReport>")

        self.dataset_output(level+1);
        self.organisms_output(level+1);

        print("</organismsReport>")

dataset = Dataset("Example2.fq", "Homo2", "sapiens", "human2", "9696", 
                  "eukaryota, ...; Homo", "Whole Blood2", "DNA", "single-end", "Roche 454")
organisms = [Organism("1336767", "95.678", "9606", "eukarioti .... homo2", "Host2", "Kuga",
                      "tuberkuloza", "", "", "")] * 5

xml = XMLOutput(dataset, organisms) 
xml.xml_output(0);
