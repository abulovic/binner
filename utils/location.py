

class Location(object):
    def __init__(self):
        self.complement=False
        self.sublocations = []
    
    def intersects(self, location):
        if location.complement != self.complement:
            return False
        for sl in self.sublocations:
            for ll in location.sublocations:
                if sl[0] <= ll[0] and sl[1] >= ll[0]:
                    return True
                elif sl[0] <= ll[1] and sl[1] >= ll[1]:
                    return True
                elif ll[0] <= sl[0] and ll[1] >= sl[1]:
                    return True
                else:
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
            
    
    def find_intersection (self, location_tuple):
        loc = Location()
        loc.complement = self.complement
        if not self.intersects(Location.from_location(location_tuple, self.complement)):
            return loc
        ''' Find intersection with all the sublocations '''