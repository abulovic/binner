from utils.autoassign import autoassign

class Dataset(object):

    @autoassign
    def __init__(self, name, host_genus, host_species, common_name, taxon_id, 
                 taxonomy, sample_source, sample_type, seq_method, sequencer):
        ''' Dataset init
            @param name input file name
            @param host_genus host genus name
            @param host_species host species name
            @param common_name common name
            @param taxon_id host taxon id
            @param taxonomy host taxonomy
            @param sample_source e.g. Whole Blood
            @param sample_type e.g. DNA
            @param seq_method e.g. single-end
            @param sequncer Roche 454, Illumina, PacBio or IonTorrent
        '''
        pass

class Gene(object):

    @autoassign
    def __init__(self, protein_id, locus_tag, product, name):
        ''' Gene init
            @param protein_id protein id e.g. AAS63914.1
            @param locus_tag e.g. YP_3766
            @param product e.g. putative carbohydrate kinase
            @param name gene name e.g. xylB3
        '''
        pass
        
class Variant(object) :

    @autoassign
    def __init__(self, ref_name, ref_start, ref_seq, name, offset, context):
        ''' Variant init
            @param ref_name e.g. CAB54900.1
            @param ref_start e.g. 31
            @param ref_seq e.g. -
            @param name variant name e.g. A
            @param offset e.g. 28
            @param context e.g. ACTGGGGAGAGAGGAGCTTTTATATATATATTATAAGGCCC  
        '''
        pass

class Organism(object):

    @autoassign
    def __init__(self, amount_count, amount_relative, taxon_id, taxonomy, name,
                 genus, species, genes, variants, reads, is_host=False):
        ''' Organism init
            @param amount_count amount of reads e.g. 2156
            @param amount_relative relative to all others e.g. 0.158
            @param taxon_id e.g. 9606 for human
            @param taxonomy organism taxonomy
            @param name organism name e.g. Yersinia
            @param species organism species
            @param ([Gene]) genes list of genes
            @param ([Variant]) variants list of variants
            @param ([Read]) reads list of reads
            @param is_host a bool defining whether the organism is host or not
        '''
        pass

class Read(object):

    @autoassign
    def __init__(self, sequence):
        pass

class XMLOutput(object):

    def __init__(self, dataset, organisms):
        ''' XMLOutpu init
            @param (Dataset) dataset structure with info about the dataset
            @param ([Organism]) organisms a list of all organims and coresponding data
        '''
        self.dataset = dataset
        self.organisms = organisms

    def _dataset_details_output(self, level):

        tab = " " * level * 2

        print(tab + "<datasetName>" + str(self.dataset.name) + "</datasetName>")
        print(tab + "<hostGenus>" + str(self.dataset.host_genus) + "</hostGenus>")
        print(tab + "<hostSpecies>" + str(self.dataset.host_species) + "</hostSpecies>")
        print(tab + "<commonName>" + str(self.dataset.common_name) + "</commonName>")
        print(tab + "<taxonomy taxon_id=\"" + str(self.dataset.taxon_id)  + "\">" + str(self.dataset.taxonomy) + "</taxonomy>")
        print(tab + "<sampleSource>" + str(self.dataset.sample_source) + "</samleSource>")
        print(tab + "<sampleType>" + str(self.dataset.sample_type) + "</sampleType>")
        print(tab + "<sequencer method=\"" + str(self.dataset.seq_method) + "\">" + str(self.dataset.sequencer) + "</sequencer>")

    def _dataset_output(self, level):
        
        tab = " " * level * 2

        print(tab + "<dataset>")
        self._dataset_details_output(level+1)
        print(tab + "</dataset>")

    def _gene_output(self, level, gene):

        tab = " " * level * 2

        print(tab + "<gene protein_id=\"" + str(gene.protein_id) + "\" locus_tag=\"" + str(gene.locus_tag) + "\" product=\"" + str(gene.product) + "\">" + str(gene.name) + "</gene>" )

    def _variant_details(self, level, variant):

        tab = " " * level * 2

        print(tab + "<variant ref_name=\"" + str(variant.ref_name) + "\" ref_start=\"" + str(variant.ref_start) + "\" ref_seq=\"" + str(variant.ref_seq) + "\">" + str(variant.name) + "</variant>")
        print(tab + "<context offset=\"" + str(variant.offset) + "\">" + str(variant.context) + "</context>")

    def _variant_output(self, level, variant):

        tab = " " * level * 2

        print(tab + "<sequenceDifference>")
        self._variant_details(level+1, variant)
        print(tab + "</sequenceDifference>")

    def _sequence_output(self, level, read):

        tab = " " * level * 2

        print(tab + "<sequence>" + str(read.sequence) + "</sequence>")

    def _organism_details_output(self, level, organism):

        tab = " " * level * 2

        print(tab + "<relativeAmount count=\">" + str(organism.amount_count) + "\">" + str(organism.amount_relative) + "</relativeAmount>")
        print(tab + "<taxonomy taxon_id=\"" + str(organism.taxon_id) + "\">" + str(organism.taxonomy) + "</taxonomy>")
        print(tab + "<organsimName>" + str(organism.name) + "</organismName>")

        if organism.is_host:
            # rest of data not needed in this case
            return

        print(tab + "<genus>" + str(organism.genus) + "</genus>")
        print(tab + "<species>" + str(organism.species) + "</species>")

        print(tab + "<genes>")
        for gene in organism.genes:
            self._gene_output(level+1, gene)
        print(tab + "<genes>")

        print(tab + "<variants>")
        for variant in organism.variants:
            self._variant_output(level+1, variant)
        print(tab + "</variants>")

        print(tab + "<reads>")
        for read in organism.reads:
            self._sequence_output(level + 1, read)
        print(tab + "</reads>")

    def _organism_output(self, level):

        tab = " " * level * 2

        for organism in self.organisms:
            print(tab + "<organism>")
            self._organism_details_output(level+1, organism)
            print(tab + "</organism>")

    def _organisms_output(self, level):

        tab = " " * level * 2

        print(tab + "<organisms>")
        self._organism_output(level+1)
        print(tab + "</organisms>")

    def xml_output(self, level=0):
        ''' Generates the xml from data already present in dataset and organisms
            to stdout
            @param level default 0, start offset for level zero xml tags
        '''

        print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
        print("<organismsReport>")
        self._dataset_output(level+1);
        self._organisms_output(level+1);
        print("</organismsReport>")
