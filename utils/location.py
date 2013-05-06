
class Location(object):
    def __init__(self, sublocations=None, complement=None):
        if complement:
            self.complement = complement
        else:
            self.complement=False
        if sublocations:
            self.sublocations = sublocations
        else:
            self.sublocations = []
    
    def intersects(self, location):
        """
        @return (boolean) True if object intersects with location, otherwise false.
        """
        if location.complement != self.complement:
            return False
        for sl in self.sublocations:
            for ll in location.sublocations:
                if not(sl[0] > ll[1] or ll[0] > sl[1]):
                    return True
        return False
    
    @classmethod
    def _parse_sublocation(self, location, tolerance):
        tokens = location.split('..')
        l = []
        for token in tokens:
            if token.startswith('>'):
                l.append(int(token[1:])+tolerance)
            elif token.startswith('<'):
                l.append(int(token[1:])-tolerance)
            else:
                l.append(int(token)) 
        if len(l) == 2:
            return tuple(l)
    
    @classmethod
    def from_location_str(cls, location_str, tolerance=0):
        location = Location()
        
        
        line = location_str.strip()
        while line:
            if line.startswith('complement'):
                line=line[11:-1]
                location.complement=True
                continue
            elif line.startswith('join'):
                line=line[5:-1]
                tokens=line.split(',')
                for token in tokens:
                    l = cls._parse_sublocation(token, tolerance)
                    location.sublocations.append(l)
                break
            else:
                l = cls._parse_sublocation(line, tolerance)
                location.sublocations.append(l)
                break
        
        return location
            
    @classmethod
    def from_location(cls, location=(0,0), complement=False):
        loc = Location()
        loc.complement = complement
        if len(location) != 2:
            location = (location[0], location[0])
        loc.sublocations.append(location)
        return loc
            
    
    def find_intersection (self, location_tuple, complement):
        ''' Computes intersection region between the
            supplied location and itself
            @param location Location
            @return None if the supplied locations don't intersect,
                    otherwise returns the location object with 
                    locations of intersection
        '''
        test_loc = Location()
        test_loc.complement = complement
        test_loc.sublocations.append(location_tuple)

        if not self.intersects(test_loc):
            return None

        loc = Location (complement=complement)

        (target_start,target_stop) = location_tuple
        # Find all intersections
        for (sub_start, sub_stop) in self.sublocations:
            if not(target_start > sub_stop or sub_start > target_stop): # If they intersect
                loc.sublocations.append((max(target_start, sub_start), min(target_stop, sub_stop)))

        # Found no intersection
        if len(loc.sublocations) == 0:
            return None
        return loc

    def __str__(self):
        return str(self.complement) + " " + str(self.sublocations)

    def length(self):
        """
        @return Number of bases covered (Sum of lengths of all sublocations).
        """
        ret = 0
        for subloc in self.sublocations:
            ret += subloc[1] - subloc[0] + 1
        return ret
