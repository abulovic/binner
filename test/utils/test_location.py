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
        
    def testInstersectionWithoutComplementInformation(self):
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('complement(5..15)')
        
        self.assertTrue(l1.intersects(l2, use_complement=False),
                         'The locations should intersect')
        self.assertFalse(l1.intersects(l2, use_complement=True),
                         "The locations should't intersect")
        
    def testLocationContains(self):
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('5..10')
        
        self.assertTrue(l1.contains(l2), 
                        '1..10 should contain 5..10')
        
        l1 = Location.from_location_str('complement(<23..50)')
        l2 = Location.from_location_str('complement(24..50)')
        
        self.assertTrue(l1.contains(l2), 
                        'complement(<23..50) should contain ' 
                        'complement(24..50)')
        
        l1 = Location.from_location_str('join(1..10,20..30)')
        l2 = Location.from_location_str('join(2..8,25..28)')
        
        self.assertTrue(l1.contains(l2), 
                        'join(1..10,20..30) should contain ' 
                        'join(2..8,25..28)')
        
        l1 = Location.from_location_str(
                        'join(complement(1..10),complement(20..30))')
        l2 = Location.from_location_str(
                        'join(complement(2..8),complement(25..28))')
        
        self.assertTrue(l1.contains(l2), 
                'join(complement(1..10),complement(20..30)) should contain ' 
                'join(complement(2..8),complement(25..28))')
        
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('4..20')
        
        self.assertFalse(l1.contains(l2), 
                        '1..10 should not contain ' 
                        '4..20')
        
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('15..20')
        
        self.assertFalse(l1.contains(l2), 
                        '1..10 should not contain ' 
                        '15..20')
        
        l1 = Location.from_location_str('complement(1..10)')
        l2 = Location.from_location_str('complement(4..20)')
        
        self.assertFalse(l1.contains(l2), 
                        'complement(1..10) should not contain ' 
                        'complement(4..20)')
        
        l1 = Location.from_location_str('complement(1..10)')
        l2 = Location.from_location_str('complement(15..20)')
        
        self.assertFalse(l1.contains(l2), 
                        'complement(1..10) should not contain ' 
                        'complement(15..20)')
        
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('complement(1..10)')
        
        self.assertFalse(l1.contains(l2), 
                        '1..10 should not contain ' 
                        'complement(1..10)')
        
        l1 = Location.from_location_str('1..10')
        l2 = Location.from_location_str('complement(15..20)')
        
        self.assertFalse(l1.contains(l2), 
                        '1..10 should not contain ' 
                        'complement(15..20)')
        
        l1 = Location.from_location_str('join(1..10,11..50)')
        l2 = Location.from_location_str('15..20')
        
        self.assertTrue(l1.contains(l2), 
                        'join(1..10,11..50) should contain ' 
                        '15..20')
        
        l1 = Location.from_location_str('join(1..10,11..50)')
        l2 = Location.from_location_str('complement(15..20)')
        
        self.assertTrue(l1.contains(l2, use_complement=False), 
                        'join(1..10,11..50) should contain ' 
                        'complement(15..20) without complement information')
        
        l1 = Location.from_location_str('REF1:1..10')
        l2 = Location.from_location_str('5..10')
        
        self.assertFalse(l1.contains(l2), 
                        'REF1:1..10 should contain 5..10')
        
        l1 = Location.from_location_str('REF1:1..10')
        l2 = Location.from_location_str('REF2:5..10')
        
        self.assertFalse(l1.contains(l2), 
                        '1..10 should contain 5..10')
    
    def testLocationMinimum(self):
        l1 = Location.from_location_str('join(1..10,11..50)')
        l2 = Location.from_location_str('complement(15..20)')
        l3 = Location.from_location_str('REF2:5..10')
        l4 = Location.from_location_str('complement(join(1..10,11..50))')
        l5 = Location.from_location_str('complement(join(15..20,1..2))')
        
        self.assertEqual(l1.min(), 1, 'Minimum should be 1')
        self.assertEqual(l2.min(), 15, 'Minimum should be 15')
        self.assertEqual(l3.min(), 5, 'Minimum should be 5')
        self.assertEqual(l4.min(), 1, 'Minimum should be 1')
        self.assertEqual(l5.min(), 1, 'Minimum should be 1')
        
    def testFastMinimum(self):
        l1 = Location.fast_min_str('join(1..10,11..50)')
        l2 = Location.fast_min_str('complement(15..20)')
        l3 = Location.fast_min_str('REF2:5..10')
        l4 = Location.fast_min_str('complement(join(1..10,11..50))')
        l5 = Location.fast_min_str('complement(join(15..20,1..2))')
        
        self.assertEqual(l1, 1, 'Minimum should be 1')
        self.assertEqual(l2, 15, 'Minimum should be 15')
        self.assertEqual(l3, 5, 'Minimum should be 5')
        self.assertEqual(l4, 1, 'Minimum should be 1')
        self.assertEqual(l5, 1, 'Minimum should be 1')
        
    def testLocationOverlap(self):
        l1 = Location.from_location_str('join(1..10,11..50)')
        l2 = Location.from_location_str('complement(join(1..2,15..20))')
        
        self.assertEqual(1, l1.start, "Start should be 1")
        self.assertEqual(50, l1.end, "End should be 50")
        
        self.assertEqual(1, l2.start, "Start should be 1")
        self.assertEqual(20, l2.end, "End should be 20")
        
        self.assertTrue(l1.overlaps(l2, use_complement=False),
                        'Locations should overlap')
        
        self.assertTrue(l1.overlaps(l2, use_complement=True),
                        "Locations shouldn't overlap")
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIntersections']
    unittest.main()