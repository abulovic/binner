
from data.alignment import ReadAlnLocation

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
        # Attributes for creating new read
        newRead_id       = None
        newRead_length   = None # Not available for now, should be in the future
        newRead_aln_locs = []

        # valList: ["read_id, num_align", "alignInfo1", "alignInfo2", ... "alignInfoN"]
        valList = read_str.split(';');
        valList.pop(); # Pop the last element, '\n'

        # Get header info
        # headerList: [read_id, num_align]
        headerList = valList[0].split(',');
        newRead_id = headerList[0];
        num_align = headerList[1];
        
        # Store every alignInfo
        for alignInfo in valList[1:]:
            data = alignInfo.split(','); # [nucl_acc, db_source, GI, score, start, stop, strand]

            nucl_acc    = data[0]
            db_source   = data[1]
            GI          = int   (data[2])
            score       = float (data[3])
            start       = int   (data[4])
            stop        = int   (data[5])
            strand      = data[6]

            complement  = False if strand=='+' else True

            # Create and store new ReadAlnLocation object
            newAlignInfo = ReadAlnLocation(newRead_id, nucl_acc, db_source, GI, score,
                                           (start, stop), complement);
            # temporary fix
            if db_source == 'dbj': continue
            newRead_aln_locs.append(newAlignInfo);

        return Read(newRead_id, newRead_length, newRead_aln_locs)
    
    def set_type (self):
        """ Read can be aligned or unaligned
        """
        pass
