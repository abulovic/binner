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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIntersections']
    unittest.main()