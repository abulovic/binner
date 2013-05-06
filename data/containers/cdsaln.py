from utils.singleton        import Singleton
from data.containers.record import RecordContainer
from data.alignment         import CdsAlignment

from collections            import defaultdict

@Singleton
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
        self.record_repository = RecordContainer.Instance()

    

    def populate (self, read_cont):

        # Iterate through reads
        num = 0;
        for read in read_cont.read_repository.values():

            # Iterate through read alignments
            for readAln in read.alignment_locations:

                if not readAln.active:
                    continue
                
                # Iterate through aligned CDSs for each read alignment
                for (cds, alignment_location) in readAln.aligned_cdss:
                    # if this CDS hasn't been added yet
                    if not self.cds_repository.has_key (cds):
                        cds_alignment = CdsAlignment (cds)
                        cds_alignment.add_aligned_sublocation (read.id, alignment_location, readAln.score)
                        self.cds_repository[cds] = cds_alignment
                        self.read2cds[read.id].append(cds_alignment)
                    # CDS already exists in the cds repository
                    else:
                        cds_alignment = self.cds_repository[cds]
                        # CDS already contains subalignment with this read, pass 
                        if cds_alignment.contains_read (read.id):
                            continue
                        else:
                            cds_alignment.add_aligned_sublocation (read.id, alignment_location, readAln.score)

        print "pogledao sam alignova: %d " % num


    def printSelf(self):
        for cds_aln in self.cds_repository.values():
            print str(cds_aln.cds.record_id) + " " + str(cds_aln.cds.location)
            for aln_reg in cds_aln.aligned_regions.values():
                print "    " + str(aln_reg.active) + " " + str(aln_reg.location.sublocations) + " " + str(aln_reg.read_id)

