def dataset_details_output(level):
    
    tab = " " * level * 2
    dataSetName = "Example1.fq"
    hostGenus = "Homo"
    hostSpecies = "sapiens"
    commonName = "human"
    taxon_id = "9606"
    taxonomy = "Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini; Catarrhini; Hominidae; Homo."
    sampleSource = "Whole Blood"
    sampleType = "DNA"
    seq_method = "single-end"
    sequencer = "Roche 454"
 
    print(tab + "<datasetName>" + dataSetName + "</datasetName>")
    print(tab + "<hostGenus>" + hostGenus + "</hostGenus>")
    print(tab + "<hostSpecies>" + hostSpecies + "</hostSpecies>")
    print(tab + "<commonName>" + commonName + "</commonName>")
    print(tab + "<taxonomy taxon_id=\"" + taxon_id  + "\">" + taxonomy + "</taxonomy>")
    print(tab + "<sampleSource>" + sampleSource + "</samleSource>")
    print(tab + "<sampleType>" + sampleType + "</sampleType>")
    print(tab + "<sequencer method=\"" + seq_method + "\">" + sequencer + "</sequencer>")

    return

def dataset_output(level):

    tab = " " * level * 2

    print(tab + "<dataset>")
    dataset_details_output(level+1)
    print(tab + "</dataset>")

    return

def gene_output(level):

    tab = " " * level * 2
    protein_id = "AAS638912.1"
    locus_tag = "YP_3766"
    product = "carbohidrati neke vrste"
    gene = "xy567"

    print(tab + "<gene protein_id=\"" + protein_id + "\" locus_tag=\"" + locus_tag + "\" product=\"" + product + "\">" + gene + "</gene>" )

    return

def variant_details(level):

    tab = " " * level * 2
    ref_name = "CAB78909.1"
    ref_start = "31"
    ref_seq = "-"
    variant = "A"
    offset = "28"
    genome_sequence = "ACTGATTTTTGGGGATAGTAGATGATGATCCAGTGATAG"

    print(tab + "<variant ref_name=\"" + ref_name + "\" ref_start=\"" + ref_start + "\" ref_seq=\"" + ref_seq + "\">" + variant + "</variant>")
    print(tab + "<context offset=\"" + offset + "\">" + genome_sequence + "</context>")

    return

def variant_output(level):

    tab = " " * level * 2
 
    print(tab + "<sequenceDifference>")
    variant_details(level+1)
    print(tab + "</sequenceDifference>")

    return

def sequence_output(level):
    
    tab = " " * level * 2
    sequence = "HT8943589J"

    print(tab + "<sequence>" + sequence + "</sequence>")

    return

def organism_details_output(level, is_host=False):

    tab = " " * level * 2
    count = "1332476"
    rel_amount = "97.482"
    taxon_id = "9606"
    taxonomy = "Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini; Catarrhini; Hominidae; Homo."
    organism_name = "Host"

    print(tab + "<relativeAmount count=\">" + count + "\">" + rel_amount + "</relativeAmount>")
    print(tab + "<taxonomy taxon_id=\"" + taxon_id  + "\">" + taxonomy + "</taxonomy>")
    print(tab + "<organimName>" + organism_name + "</organismName>")

    if is_host:
        return

    genus = "Yersinia"
    species = "pseudotuberculosis"

    print(tab + "<genus>" + genus + "</genus>")
    print(tab + "<species>" + species + "</species>")

    print(tab + "<genes>")
    # za svaki gen ispis ga, for petlja treba biti
    gene_output(level+1)
    print(tab + "<genes>")

    print(tab + "<variants>")
    # za svaku varijantu ispis, for petlja treba bit
    variant_output(level+1)
    print(tab + "</variants>")

    print(tab + "<reads>")
    sequence_output(level + 1)
    print(tab + "</reads>")

    return

def organism_output(level):

    tab = " " * level * 2

    print(tab + "<organism>")

    organism_details_output(level+1, True)

    # ovdje sad idu paraziti, znaci for petlja
    # za svaki parazit ispisi njegov xml
    organism_details_output(level+1)
    
    print(tab + "</organism>")

    return

def organisms_output(level):

    tab = " " * level * 2

    print(tab + "<organisms>")
    organism_output(level+1)
    print(tab + "</organisms>")
  
    return

def xml_output(level):

    print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
    print("<organismsReport>")

    dataset_output(level+1);
    organisms_output(level+1);

    print("</organismsReport>")
    return

xml_output(0);
