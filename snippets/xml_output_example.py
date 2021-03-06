import sys, os
sys.path.append(os.getcwd())

from formats.xml_output import *

if (len(sys.argv)<3):
    print "Usage: python snippets/xml_output_example.py <DATASET_DESC_XML_FILE> <XML_OUTPUT_FILE>"
    sys.exit(-1)

dataset = Dataset(sys.argv[1]) 

hostOrganism = [Organism(8888888, 0.957878, "9606", "eukaritoi ... tralala", 
                         "host", "", "", "", "", "", True)]

organisms = hostOrganism

for i in range(0, 7):
    # adding same genes, variants and reads multiple times just for testing
    genes = [Gene("AA898989.1", "YP_67676", "neki karbohidrati i to", "refname_neki", "naziv gena")]*3
    # 3 times the same gene just for testing
    variants = [Variant("CAB789879", "31", "-", "A", "28", "GGGGGGGGGGGGGGG" )]*7
    # 7 times the same variant just for testing
    reads = [Read("HT89898989")]*11
    # 11 times the same read for testing purpose
    organisms = organisms + [
            Organism(1336767, 0.3234, "9606", "eukarioti .... homo2", "Host2", 
                      "Kuga","tuberkuloza", genes, variants, reads)
            ]
    # adding organism to organisms list

# organisms now consist of host organism and 8 same parasite organisms

xml = XMLOutput(dataset, organisms, sys.argv[2]) 
# init with xml data: dataset and organisms 

xml.xml_output();
# generate output on stdout
