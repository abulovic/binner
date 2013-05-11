# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2013

@author: marin
'''
import unittest
from utils.location import Location, LoactionParsingException

class Test(unittest.TestCase):


    def testIntersections(self):
        location = Location.from_location_str(
            "complement(join(<197..1301,2070..>2451))")
        
        self.assertFalse(location.intersects(
            Location.from_location((100,))))
        
        self.assertFalse(location.intersects(
            Location.from_location((100,), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((300,))))
        
        self.assertTrue(location.intersects(
            Location.from_location((300,), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((50,100))))
        
        self.assertFalse(location.intersects(
            Location.from_location((50,100), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((300,400))))
        
        self.assertTrue(location.intersects(
            Location.from_location((300,400), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((1200,1400))))
        
        self.assertTrue(location.intersects(
            Location.from_location((1200,1400), complement=True)))

    def testIntersectionsWithTolerance(self):
        location = Location.from_location_str(
            "complement(join(<197..1301,2070..>2451))", tolerance=100)
        
        self.assertFalse(location.intersects(
            Location.from_location((100,))))
        
        self.assertTrue(location.intersects(
            Location.from_location((100,), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((300,))))
        
        self.assertTrue(location.intersects(
            Location.from_location((300,), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((50,100))))
        
        self.assertTrue(location.intersects(
            Location.from_location((50,100), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((300,400))))
        
        self.assertTrue(location.intersects(
            Location.from_location((300,400), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((1200,1400))))
        
        self.assertTrue(location.intersects(
            Location.from_location((1200,1400), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((2500,2600))))
        
        self.assertTrue(location.intersects(
            Location.from_location((2500,2600), complement=True)))
        
        self.assertFalse(location.intersects(
            Location.from_location((3000,4000))))
        
        self.assertFalse(location.intersects(
            Location.from_location((3000,4000), complement=True)))
        
    def testSingleLocation(self):
        location = Location.from_location_str('join(311,400..854)')
        
        self.assertTrue(location.intersects(
            Location.from_location((311,))), 
            "Location doesn't contain target point")
        
        location = Location.from_location_str('join(14424..14857,1)')
        self.assertTrue(location.intersects(
            Location.from_location((1,))),
            "Location doesn't contain target point")
        
    def testSingleLocationWithTolerance(self):
        location = Location.from_location_str(
            'join(<10,61..86,162..203,264..318,388..>495)', tolerance=10)
        
        self.assertTrue(location.intersects(
            Location.from_location((5,))),
            "Location doesn't contain target point")
        
        location = Location.from_location_str(
            'join(<1..129,>657)', tolerance=10)
        
        self.assertTrue(location.intersects(
            Location.from_location((660,))),
            "Location doesn't contain target point")

    def testParsesLocationWithSpaces(self):
        location = Location.from_location_str(
            'join(620..987, 1010..1170,1194..1443)')
        
        self.assertTrue(location.intersects(
            Location.from_location((1010,))), 
            "Location doesn't contain target point")
    
    def testParsesMultisegmentLocation(self):
        location = Location.from_location_str(
            'join(AF178221.1:<1..60,AF178222.1:1..63,AF178223.1:1..42, 1..>90)')
        
        self.assertTrue(location.intersects(
            Location.from_location((80,))), 
            "Location doesn't contain target point")
        self.assertIn('AF178221.1', location.references(),
                      'Reference AF178221.1 not parsed')
        self.assertIn('AF178222.1', location.references(),
                      'Reference AF178222.1 not parsed')
        self.assertIn('AF178223.1', location.references(),
                      'Reference AF178223.1 not parsed')
        self.assertTrue(len(location.references())==3, 
                        'Wrong number of references')
    
    def testParseOrderLocation(self):
        location = Location.from_location_str('order(1..3,4..6)')
        self.assertTrue(location.intersects(
            Location.from_location((3,4))),
            "Location doesn't contain target point")
        
    def testFailsParsingSiteBetweenLocation(self):
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, '1^2')
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, 'AL121804:41^42')
    
    def testFailsParsingSingleResidueLocation(self):
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, '1.2')
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, '(3.9)..10')
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, '26..(30.33)')
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, '(13.19)..(20.28)')
        
    def testFailsParsingOneOfLocation(self):
        self.assertRaises(LoactionParsingException, 
                          Location.from_location_str, 'one-of(3,6)..101')
    
    def testParseReferenceLocation(self):
        location = Location.from_location_str('REFERENCE:1..10')
        self.assertTrue(location.intersects(Location.from_location((5,15))))
        
    def testFailsParseMixedStrands(self):
        self.assertRaises(LoactionParsingException,
                          Location.from_location_str, 
                          'join(34533..34918,complement(316490..316748))')
    def testIntersectionDifferentStrands (self):
        loc1 = Location.from_location(location_tuple=(1,2), complement=True)
        loc2 = Location.from_location(location_tuple=(1,2), complement=False)
        self.assertEqual (None, loc1.find_intersection(loc2))

    def testIntersectionLocation (self):

        # Test no intersection case
        loc1 = Location.from_location_str('complement(50..100)')
        self.assertEqual (None, loc1.find_intersection(
                          Location.from_location_str('complement(200..500)')))
        self.assertEqual (None, loc1.find_intersection(
                          Location.from_location_str('complement(1..40)')))
        self.assertEqual (None, loc1.find_intersection(
                          Location.from_location_str('complement(1..49)')))
        self.assertEqual (None, loc1.find_intersection(
                          Location.from_location_str('complement(101..150)')))

        # Test simple one interval intersection
        loc1 = Location.from_location_str('10..100')
        loc2 = Location.from_location_str('50..100')
        intersection = loc1.find_intersection(loc2)
        self.assertEqual(loc2.start, intersection.start, 
                         "Start intersection position doesn't match")
        self.assertEqual(loc2.end, intersection.end, 
                         "End intersection position doesn't match")
        self.assertEqual(loc2.complement, intersection.complement, 
                         "Complement intersection information doesn't match")

        # Test multiple interval intersection
        loc1 = Location.from_location_str('join(1..40,60..80,120..200)')
        aln_location = Location.from_location_str('30..130')
        loc2 = Location.from_location_str('join(30..40,60..80,120..130)')
        intersection = loc1.find_intersection(aln_location)
        for subint, subl2 in zip(intersection.sublocations, loc2.sublocations):
            self.assertEqual(subl2.start, subint.start, 
                             "Start intersection position doesn't match")
            self.assertEqual(subl2.end, subint.end, 
                             "End intersection position doesn't match")
        self.assertEqual(loc2.complement, intersection.complement,
                         "Complement intersection information doesn't match")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIntersections']
    unittest.main()