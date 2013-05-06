import sys, os
sys.path.append(os.getcwd())

from formats.xml_output import *

dataset = Dataset("Example2.fq", "Homo2", "sapiens", "human2", "9696", 
                  "eukaryota, ...; Homo", "Whole Blood2", "DNA", "single-end", "Roche 454")

genes = [Gene("AA898989.1", "YP_67676", "neki karbohidrati i to", "naziv gena")]*3
# 3 times the same gene just for testing

variants = [Variant("CAB789879", "31", "-", "A", "28", "GGGGGGGGGGGGGGG" )]*7
# 7 times the same variant just for testing

reads = [Read("HT89898989")]*11
# 11 times the same read for testing purpose

hostOrganism = [Organism("8888888", "95.7878", "9606", "eukaritoi ... tralala", 
                         "host", "", "", "", "", "", True)]

organisms = hostOrganism + [
            Organism("1336767", "0.3234", "9606", "eukarioti .... homo2", "Host2", 
                      "Kuga","tuberkuloza", genes, variants, reads)
            ] * 5
# organisms consist of host organism and 11 same parasite organisms

xml = XMLOutput(dataset, organisms) 
# init with xml data: dataset and organisms 

xml.xml_output();
# generate output on stdout
