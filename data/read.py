class Read (object):
    """ Contains all the read-related information, 
        such as the its identifier and the list of alignment
        locations
    """
    
    def __init__ (self, read_id, read_length, alignment_locations):
        self.id                     = read_id
        self.length                 = read_length
        self.alignment_locations    = alignment_locations
    
    @staticmethod
    def from_read_str (read_str):
        """ Parses the description string and creates a new read from it with 
            accompanying alignment locations
        """
        pass
    
    def set_type (self):
        """ Read can be aligned or unaligned
        """
        pass