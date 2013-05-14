from collections            import defaultdict

from data.containers.record import RecordContainer
from data.alignment         import CdsAlignment

class CdsAlnContainer (object):
    ''' CDS Alignment Container serves as the storage for all 
        CDSs reported in the read alignments. 
        CDS alignment is mapped using record id and cds location 
        and can be fetched using the tuple containing 
        (record_id, location)
    '''

    def __init__(self):
        self.cds_repository = {}
        self.read2cds       = defaultdict(list)    

    def populate (self, read_cont):
        '''
        Populates CDS container from read container. 
        Iterates through every read, and for each read it goes through 
        all the read alignments. For each alignment, it goes through all the
        locations where the alignments intersects a CDS.
        Each intersected cds will be contained within a CdsALignment object
        where all the reads mapped to the particular cds are contained. 
        It is possible to extract cds alignment by using cds as a key, and
        it is also possible to find all the CdsAlignments cointaining a 
        particular read using the read identifier as a key.
        '''
        # Iterate through reads
        for read in read_cont.read_repository.values():
            # Iterate through read alignments
            for readAln in read.alignment_locations:
                if not readAln.active:
                    continue
                # Iterate through aligned CDSs for each read alignment
                for (cds, alignment_location) in readAln.aligned_cdss:
                    # if this CDS hasn't been added yet
                    if not self.cds_repository.has_key (cds):
                        cds_alignment            = CdsAlignment (cds)
                        cds_alignment.add_aligned_sublocation (read.id, alignment_location, readAln.score)
                        self.cds_repository[cds] = cds_alignment
                    else:
                        cds_alignment            = self.cds_repository[cds]
                        # check whether CDS alignment contains this read or not
                        if cds_alignment.contains_read (read.id):
                            continue
                        else:
                            cds_alignment.add_aligned_sublocation (read.id, alignment_location, readAln.score)
                    self.read2cds[read.id].append(cds_alignment)

    def __str__(self):
        tab = " " * 2
        ret = "CdsAlignmentContainer\n"
        ret += tab + "cds_repository:\n"
        for (key, cds_aln) in self.cds_repository.items():
            ret += tab * 2 + "(key) " + str(key).replace("\n", "\n"+(tab*2)) + ":\n"
            ret += tab * 3 + str(cds_aln).replace("\n", "\n"+(tab*3)) + "\n"
        ret += tab + "read2cds:\n"
        for (read_id, cds_alns) in self.read2cds.items():
            ret += tab * 2 + "(key) " + str(read_id) + ":\n"
            for cds_aln in cds_alns:
                ret += tab * 3 + "CdsAlignmentContainer:\n"
                ret += tab * 4 + "cds: " + str(cds_aln.cds) + "\n"
        return ret


    def fetch_all_cds_alns (self):
        '''
        Fetches iterator over all cds alignments from the
        cds alignment repository
        '''
        return iter(self.cds_repository.values())

