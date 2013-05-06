import sys, os
sys.path.append(os.getcwd())

import unittest, random
from ncbi.taxonomy.tree import TaxTree
from ncbi.db.access import DbQuery

class TaxTreeTest (unittest.TestCase):

	def setUp(self):
		self.tax_tree = TaxTree()

	def testLoaded (self):
		self.assertEqual (1, self.tax_tree.root)

	def testIsChild (self):
		node1 = self.tax_tree.bacteria
		node2 = node1
		for i in xrange(1,5):
			if not self.tax_tree.child_nodes.has_key(node2):
				break
			children =  self.tax_tree.child_nodes[node2]
			child_index = random.randint(0,len(children)-1)
			node2 = children[child_index]

		self.assertEqual (True, self.tax_tree.is_child(node2, node1))
		self.assertEqual (False, self.tax_tree.is_child(node2, self.tax_tree.eukaryota))

	def testTaxonomyLineage (self):
		db_query = DbQuery()
		print self.tax_tree.get_taxonomy_lineage (9606, db_query)

	def testLca (self):
		# check lca for bacteria & fungi is root
		self.assertEqual (131567, self.tax_tree.find_lca ( 
				[self.tax_tree.bacteria, self.tax_tree.fungi])
														 )
		# check lca is ok for two identical child nodes (131567 - cellular organisms)
		self.assertEqual (131567, self.tax_tree.find_lca ( 
				[self.tax_tree.eukaryota, self.tax_tree.eukaryota])
														 )
		# check ordinary case. 
		root = self.tax_tree.bacteria
		lca_nodes = []
		child = root
		for i in xrange(1,20):
			if self.tax_tree.child_nodes.has_key[child]:
				children = self.tax_tree.child_nodes[child]
				child = children[random.randint(0,len(children)-1)]
				lca_nodes.append(child)
			else:
				break
		self.assertEqual (root, self.tax_tree.find_lca (lca_nodes))

if __name__ == '__main__':
	unittest.main()
