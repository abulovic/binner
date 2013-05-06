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
    def __init__(self, protein_id, locus_tag, product, name):
        pass
        
class Variant(object) :

    @autoassign
    def __init__(self, ref_name, ref_start, ref_seq, name, offset, context):
        pass

class Organism(object):

    @autoassign
    def __init__(self, amount_count, amount_relative, taxon_id, taxonomy, name,
                 genus, species, genes, variants, reads, is_host=False):
        pass

class Read(object):

    @autoassign
    def __init__(self, sequence):
        pass

class XMLOutput(object):

    def __init__(self, dataset, organisms):
        self.dataset = dataset
        self.organisms = organisms

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

    def gene_output(self, level, gene):

        tab = " " * level * 2

        print(tab + "<gene protein_id=\"" + gene.protein_id + "\" locus_tag=\"" + gene.locus_tag + "\" product=\"" + gene.product + "\">" + gene.name + "</gene>" )

    def variant_details(self, level, variant):

        tab = " " * level * 2

        print(tab + "<variant ref_name=\"" + variant.ref_name + "\" ref_start=\"" + variant.ref_start + "\" ref_seq=\"" + variant.ref_seq + "\">" + variant.name + "</variant>")
        print(tab + "<context offset=\"" + variant.offset + "\">" + variant.context + "</context>")

    def variant_output(self, level, variant):

        tab = " " * level * 2

        print(tab + "<sequenceDifference>")
        self.variant_details(level+1, variant)
        print(tab + "</sequenceDifference>")

    def sequence_output(self, level, read):

        tab = " " * level * 2

        print(tab + "<sequence>" + read.sequence + "</sequence>")

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
        for gene in organism.genes:
            self.gene_output(level+1, gene)
        print(tab + "<genes>")

        print(tab + "<variants>")
        for variant in organism.variants:
            self.variant_output(level+1, variant)
        print(tab + "</variants>")

        print(tab + "<reads>")
        for read in organism.reads:
            self.sequence_output(level + 1, read)
        print(tab + "</reads>")

    def organism_output(self, level):

        tab = " " * level * 2

        for organism in self.organisms:
            print(tab + "<organism>")
            self.organism_details_output(level+1, organism)
            print(tab + "</organism>")

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

genes = [Gene("AA898989.1", "YP_67676", "neke pizdarije karbohidrati i to", "naziv gena")]*3

variants = [Variant("CAB789879", "31", "-", "A", "28", "GGGGGGGGGGGGGGG" )]*7

reads = [Read("HT89898989")]*11

organisms = [Organism("1336767", "95.678", "9606", "eukarioti .... homo2", "Host2", "Kuga",
                      "tuberkuloza", genes, variants, reads)] * 5

xml = XMLOutput(dataset, organisms) 
xml.xml_output(0);
