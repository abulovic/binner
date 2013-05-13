import sys, os
sys.path.append(os.getcwd())

import unittest, filecmp
from formats.xml_output import *

class XMLOutputTest(unittest.TestCase):

    def testXMLOutput(self):
        dataset = Dataset("Example2.fq", "Homo2", "sapiens", "human2", "9696",
                "eukaryota, ...; Homo", "Whole Blood2", "DNA", "single-end", "Roche 454")

        hostOrganism = [Organism("8888888", "95.7878", "9606", "eukaritoi ... tralala",
                "host", "", "", "", "", "", True)]

        organisms = hostOrganism

        for i in range(0, 7):
            # adding same genes, variants and reads multiple times just for testing
            genes = [Gene("AA898989.1", "YP_67676", "neki karbohidrati i to", "naziv gena")]*3
            # 3 times the same gene just for testing
            variants = [Variant("CAB789879", "31", "-", "A", "28", "GGGGGGGGGGGGGGG" )]*7
            # 7 times the same variant just for testing
            reads = [Read("HT89898989")]*11
            # 11 times the same read for testing purpose
            organisms = organisms + [
            Organism("1336767", "0.3234", "9606", "eukarioti .... homo2", "Host2",
                    "Kuga","tuberkuloza", genes, variants, reads)            ]
            # adding organism to organisms list

        # organisms now consist of host organism and 8 same parasite organisms

        xml = XMLOutput(dataset, organisms)
        # init with xml data: dataset and organisms 

        orig_stdout = sys.stdout
        out_file = file('test/formats/test_file_xml', 'w')
        sys.stdout = out_file
        # redirect print output to file
        xml.xml_output()
        sys.stdout = orig_stdout
        out_file.close()
        self.assertEqual (True, filecmp.cmp('test/formats/test_file_xml', 'test/formats/xml/test_out.xml'))
        os.system("rm test/formats/test_file_xml")

if __name__ == '__main__':
    unittest.main()
