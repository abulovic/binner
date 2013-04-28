import sys, os
sys.path.append(os.getcwd())

import unittest
from utils.location import Location

class LocationTest (unittest.TestCase):

	def setUp(self):
		pass

	def test_different_strands (self):
		loc1 = Location(complement=True)
		self.assertEqual (None, loc1.find_intersection((0,0), False))

	def test_no_intersection (self):
		loc1 = Location(sublocations=[(50,100)], complement=True)

		self.assertEqual (None, loc1.find_intersection((200,500), True))
		self.assertEqual (None, loc1.find_intersection((1,40), True))
		self.assertEqual (None, loc1.find_intersection((1,50), True))
		self.assertEqual (None, loc1.find_intersection((100,150), True))

	
	def test_simple_intersection (self):
		loc1 = Location (sublocations=[(10,100)], complement=False)
		loc3 = Location (sublocations=[(50,100)], complement=False)

		self.assertEqual (loc3.sublocations, loc1.find_intersection((50,200), False).sublocations)

	def test_intersection (self):
		loc1 = Location (sublocations=[(1,40),(60,80),(120,200)])
		aln_location = (30,130)
		loc2 = Location (sublocations=[(30,40),(60,80),(120,130)])

		self.assertEqual (loc2.sublocations, loc1.find_intersection(aln_location, False).sublocations)

if __name__ == '__main__':
	unittest.main()