'''
Module serves as a utility to analyse xml outputs, and compare 
datasets from different files.
'''
import sys, os 
sys.path.append(os.getcwd())
import xml.etree.ElementTree as ET
import argparse

from utils.logger import Logger
from utils.autoassign import autoassign
from ncbi.db.access import DbQuery


class Organism (object):
    @autoassign
    def __init__ (self, count, relative_amount, tax_id, taxonomy, organism_name, nearest_neighbor, genus, species, strain):
        pass
    def __hash__(self):
        return hash(self.tax_id)
    def __eq__(self, other):
        if not isinstance(other, Organism):
            return False
        return other.tax_id == self.tax_id
    def __ne__(self, other):
        return not self.__eq__(other)

class Gene (object):
    @autoassign
    def __init__ (self, protein_id, locus_tag, product, ref_name, ref_start, ref_end, gene_name):
        pass
    def __hash__(self):
        return hash(self.protein_id)
    def __eq__(self, other):
        if not isinstance(other, Gene):
            return False
        return other.protein_id == self.protein_id
    def __ne__(self, other):
        return not self.__eq__(other)



def load_as_xml (fpath):
    tree = ET.parse(fpath)
    root = tree.getroot()
    return root

def get_gene_data (xml_root):
    '''
    Goes through all the genes, extracts all relevant information
    (protein_id, locus_tag, product, ref_name, ref_start, ref_end, gene_name)
    and stores it in placeholder objects (Gene)
    @param xml_root (xml.etree.ElementTree.Element)
    @return genes (list of Gene objects)
    '''
    gene_list = []
    organisms = xml_root.find('organisms')
    for organism_node in organisms:
        genes = organism_node.find('genes')
        if not genes: 
            continue
        for gene_node in genes:
            protein_id = gene_node.attrib.get('protein_id', "")
            locus_tag  = gene_node.attrib.get('locus_tag', "")
            product    = gene_node.attrib.get('product', "")
            ref_name   = gene_node.attrib.get('ref_name', "")
            ref_start  = gene_node.attrib.get('ref_start', "")
            ref_end    = gene_node.attrib.get('ref_end', "")
            gene_name  = gene_node.text
            if gene_name == 'None':
                gene_name = ""
            gene = Gene(protein_id, locus_tag, product, ref_name, ref_start, ref_end, gene_name)
            gene_list.append(gene)
    return gene_list



def get_organism_data (xml_root):
    ''' Goes through all organisms and stores all organism data 
        in objects.
        @param xml_root (xml.etree.ElementTree.Element)
        @return list of Organism objects
    '''
    org_list = []
    organisms = xml_root.find('organisms')
    for organism in organisms:
        # <relativeAmount count="1">7.31583483186e-07</relativeAmount>
        amount_node     = organism.find('relativeAmount')
        relative_amount = float(amount_node.text)
        count           = int(amount_node.attrib['count'])
        # <taxonomy taxon_id="315393">Viruses, dsDNA viruses, no RNA stage, Mimiviridae, Mimivirus</taxonomy>
        tax_node = organism.find('taxonomy')
        taxonomy = tax_node.text
        if tax_node.attrib.has_key('taxon_id'):
            tax_id   = int(tax_node.attrib['taxon_id'])
        else:
            tax_id = None
        # <nearestNeighbor>Enterobacteriaceae</nearestNeighbor>
        neighbor_node    = organism.find('nearestNeighbor')
        nearest_neighbor = neighbor_node.text if neighbor_node is not  None else None 
        # <organismName>Vaccinia virus</organismName>
        organism_node = organism.find('organismName')
        organism_name = organism_node.text if organism_node is not None else None
        # <genus>Vaccinia</genus>
        genus_node = organism.find('genus')
        genus      = genus_node.text if genus_node else None
        # <species>virus</species>
        species_node = organism.find('species')
        species      = species_node.text if species_node else None
        # <strain> YPIII</strain>
        strain_node = organism.find('strain')
        strain      = strain_node.text if strain_node else None

        org = Organism(count, relative_amount, tax_id, taxonomy, organism_name, nearest_neighbor, genus, species, strain)
        org_list.append(org)

    return org_list

def get_attribute_count (genes ):
    '''
    Checks for each gene how many of the gene attributes 
    are specified. Optionally checks if any of the attributes 
    are repeated, and if so, which ones.
    @param genes (list of Gene objects)
    @return (dict, key=attribute name, value=int)
    '''
    id_cnt = 0
    locus_tag_cnt = 0
    product_cnt = 0
    ref_name_cnt = 0
    ref_start_cnt = 0
    ref_end_cnt = 0
    gene_name_cnt = 0
    # attributes = ('protein_id', 'locus_tag', 'product', 'ref_name', 'ref_start', 'ref_end', 'gene_name')
    for gene in genes:
        if gene.protein_id:     id_cnt += 1
        if gene.locus_tag:      locus_tag_cnt += 1
        if gene.product:        product_cnt += 1
        if gene.ref_name:       ref_name_cnt += 1
        if gene.ref_start:      ref_start_cnt += 1
        if gene.ref_end:        ref_end_cnt += 1
        if gene.gene_name:      gene_name_cnt += 1
    return {'protein_id':id_cnt, 'locus_tag': locus_tag_cnt, 
            'product':product_cnt, 'ref_name':ref_name_cnt, 'ref_start': ref_start_cnt,
            'ref_end': ref_end_cnt, 'gene_name': gene_name_cnt}


def get_lineage_rank (organism_names, db_access):
    '''
    Fetches organism rank for each organism name in the lineage.
    @param organism_names (list[str]) list of organism names (scientific)
    @return (list[str]) list of ranks for the specified names
    '''
    ranks = []
    for organism_name in organism_names:
        if organism_name.endswith('.'):
            organism_name = organism_name[0:-1]
        rank = db_access.get_organism_rank(organism_name, by_name=True)
        ranks.append(rank)
    return ranks

def analyze_lineages (organisms):
    db_access = DbQuery()
    for organism in organisms:
        if not organism.taxonomy:
            continue
        org_names = organism.taxonomy.split('; ')
        ranks = get_lineage_rank(org_names, db_access)
        if organism.organism_name is not None:
            print "ORG_NAME:", organism.organism_name
        else:
            print "NEIGHBOR:", organism.nearest_neighbor
        print     "RANK:    ", ranks



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python xml_analysis.py <XML_BINNER_FILE> [XML_BINNER_FILE2] "
        sys.exit(0)

    fpath1 = sys.argv[1]
    fpath2 = None
    if len(sys.argv) == 3:
        fpath2 = sys.argv[2]
    
    xml1 = load_as_xml(fpath1)
    organisms = get_organism_data(xml1)
    analyze_lineages(organisms)
