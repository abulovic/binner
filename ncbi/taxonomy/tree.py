from  collections       import defaultdict
import os


class TaxTree ():
    ''' Loads the NCBI taxonomy tree, creates both
        parent-child and child-parent relations,
        enables parent-child relationship testing and
        finding the least common ancestor.
    '''

    def __init__ (self, nodes_file=None):
        ''' Locates the ncbi taxonomy file and sets the important
            taxonomy assignments (such as animalia, bacteria ecc)
            @param location of the ncbi taxonomy tree file
        '''
        
        if not nodes_file:
            nodes_file = self._h_find_taxnode_file()
        self.load(nodes_file) 
        
        #--------- RELEVANT TAXONOMY ASSIGNMENTS ----------#
        self._h_relevant_taxonomy_assignments()   

    def load (self, nodes_file):
        self.parent_nodes   = self._h_get_tax_nodes(nodes_file)
        self.child_nodes    = self._h_populate_child_nodes()
    
    def is_child (self, child_taxid, parent_taxid):
        ''' Test if child_taxid is child node of parent_taxid
            Node is not the child of itself
        '''  
        # check boundary conditions
        if child_taxid == parent_taxid:
            return False
        if parent_taxid == self.root:
            return True
        
        tmp_parent_taxid = child_taxid
        while True:
            if not self.parent_nodes.has_key(tmp_parent_taxid):
                return False
            tmp_parent_taxid = self.parent_nodes[tmp_parent_taxid]
            if tmp_parent_taxid == self.root:
                return False
            if tmp_parent_taxid == parent_taxid:
                return True
            
            

    ############ ############ ##############
    def find_lca (self, taxid_list):
        ''' Finds the lowest common ancestor of
            a list of nodes
        '''
        # each of the visited nodes remembers how many 
        # child nodes traversed it
        self.num_visited        = defaultdict(int)

        current_taxids     = taxid_list
        num_of_nodes       = len(current_taxids)

        # first check if all nodes exist (and sum up blast scores)
        for i in range (0, len(taxid_list)):
            taxid       = taxid_list[i]
            if not self.parent_nodes.has_key(taxid):
                raise Exception ("Key error, no element with id %d." % taxid)

        # now find the lowest common ancestor
        while (True):

            parent_nodes = []

            for taxid in current_taxids:

                # root node must not add itself to parent list
                if   taxid != self.root:    parent_taxid = self.parent_nodes[taxid]
                else:                        parent_taxid = None
                
                
                
                # if parent exists, append him to parent list
                # duplicates ensure that every traversal will count
                if parent_taxid:            parent_nodes.append(parent_taxid)

                self.num_visited[taxid]     += 1
                if self.num_visited[taxid] == num_of_nodes:
                    
                    self.lca_root = taxid
                    self._h_set_visited_nodes() 
                    return taxid

            # refresh current nodes
            current_taxids = parent_nodes

    def get_taxonomy_lineage (self, taxid, db_access):
        '''
        Fetches taxonomy lineage for the organism specified 
        by its taxonomy ID.
        @param taxid (int) taxonomy id
        @param db_access (DbQuery)
        @return lineage (str)
        '''

        taxonomy_lineage = []
        current_node = taxid
        while current_node != self.root:
            organism_name = db_access.get_organism_name(current_node)
            taxonomy_lineage.append (organism_name)
            current_node = self.parent_nodes[current_node]
        taxonomy_lineage.reverse()

        return "; ".join(taxonomy_lineage)
        

    def _h_get_tax_nodes        (self, nodes_file):
        '''Loads the taxonomy nodes in a dictionary
           mapping the child to parent node.
        '''
        # file format per line: child_taxid parent_taxid
        with open(nodes_file) as fd:    
            d = dict(self._h_from_parent_child_str (line) for line in fd)
        return d
    
    def _h_from_parent_child_str (self, line):
        '''Loads two integers (taxids) from a line
        '''
        key, sep, value = line.strip().partition(" ")
        if key == value: self.root = int(key)
        return int(key), int(value)
    

    def _h_set_visited_nodes (self):
        ''' Creates class for all the taxids of the nodes visited
            in the LCA tree
        '''
        self.visited_nodes = {}
        for taxid in self.num_visited:
            print self.num_visited[taxid]
            self.visited_nodes[taxid] = TaxNode (
                                                 taxid, 
                                                 self.num_visited[taxid]
                                                 )

    def _h_find_taxnode_file(self):
        ''' Searches recursively through the current
            working directory to find the ncbi_tax_tree file.
        '''
        for root, dirs, files in os.walk (os.getcwd()):
            if 'ncbi_tax_tree' in files:
                return root + ''.join(dirs) + '/ncbi_tax_tree'
            

    def _h_populate_child_nodes (self):
        ''' Populates child nodes from parent to child 
            mapping dictionary
        '''
        child_nodes = defaultdict(list)
        for (child, parent) in self.parent_nodes.items():
            child_nodes[parent].append(child)
        return child_nodes

    def _h_relevant_taxonomy_assignments (self):
        ''' Sets some of the more important taxonomy 
            assignments which can help in checking which kingdom
            an organism belongs to.
        '''

        self.bacteria      = 2
        self.eukaryota     = 2759
        self.fungi         = 4751
        self.archea        = 2157
        self.viroids       = 12884
        self.viruses       = 10239
        self.animalia      = 33208 


class TaxNode (object):
    '''
    Contains information relevant to LCA
    taxonomy tree traversal. 
    Relevant informations is:
        - number of times node has been reported in the alignment
        - blast scores for each alignment
        - best  blast score
    '''


    def __init__(self, taxid, num_traversed = None):

        self.taxid              = taxid
        self.num_traversed      = num_traversed
