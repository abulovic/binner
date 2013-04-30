# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2013

@author: marin
'''
import unittest
from utils.location import Location

class Test(unittest.TestCase):


    def testIntersections(self):
        location = Location.from_location_str("complement(join(<197..1301,2070..>2451))")
        assert(not location.intersects(Location.from_location((100,))))
        assert(not location.intersects(Location.from_location((100,), complement=True)))
        assert(not location.intersects(Location.from_location((300,))))
        assert(location.intersects(Location.from_location((300,), complement=True)))
        assert(not location.intersects(Location.from_location((50,100))))
        assert(not location.intersects(Location.from_location((50,100), complement=True)))
        assert(not location.intersects(Location.from_location((300,400))))
        assert(location.intersects(Location.from_location((300,400), complement=True)))
        assert(not location.intersects(Location.from_location((1200,1400))))
        assert(location.intersects(Location.from_location((1200,1400), complement=True)))

    def testIntersectionsWithTolerance(self):
        location = Location.from_location_str("complement(join(<197..1301,2070..>2451))", tolerance=100)
        assert(not location.intersects(Location.from_location((100,))))
        assert(location.intersects(Location.from_location((100,), complement=True)))
        assert(not location.intersects(Location.from_location((300,))))
        assert(location.intersects(Location.from_location((300,), complement=True)))
        assert(not location.intersects(Location.from_location((50,100))))
        assert(location.intersects(Location.from_location((50,100), complement=True)))
        assert(not location.intersects(Location.from_location((300,400))))
        assert(location.intersects(Location.from_location((300,400), complement=True)))
        assert(not location.intersects(Location.from_location((1200,1400))))
        assert(location.intersects(Location.from_location((1200,1400), complement=True)))
        assert(not location.intersects(Location.from_location((2500,2600))))
        assert(location.intersects(Location.from_location((2500,2600), complement=True)))
        assert(not location.intersects(Location.from_location((3000,4000))))
        assert(not location.intersects(Location.from_location((3000,4000), complement=True)))

    def testIntersectionDifferentStrands (self):
        loc1 = Location(complement=True)
        self.assertEqual (None, loc1.find_intersection((0,0), False))

    def testIntersectionLocation (self):

        # Test no intersection case
        loc1 = Location(sublocations=[(50,100)], complement=True)
        self.assertEqual (None, loc1.find_intersection((200,500), True))
        self.assertEqual (None, loc1.find_intersection((1,40), True))
        self.assertEqual (None, loc1.find_intersection((1,50), True))
        self.assertEqual (None, loc1.find_intersection((100,150), True))

        # Test simple one interval intersection
        loc1 = Location (sublocations=[(10,100)], complement=False)
        loc2 = Location (sublocations=[(50,100)], complement=False)
        self.assertEqual (loc2.sublocations, loc1.find_intersection((50,200), False).sublocations)

        # Test multiple interval intersection
        loc1 = Location (sublocations=[(1,40),(60,80),(120,200)])
        aln_location = (30,130)
        loc2 = Location (sublocations=[(30,40),(60,80),(120,130)])
        self.assertEqual (loc2.sublocations, loc1.find_intersection(aln_location, False).sublocations)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIntersections']
    unittest.main()