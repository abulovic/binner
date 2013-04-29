from utils.singleton import Singleton
from data.containers.recordcontainer import RecordContainer

@Singleton
class CdsAlnContainer (object):
    ''' CDS Alignment Repository serves as the storage for all 
        CDSs reported in the read alignments. 
        CDS alignment is mapped using record id and cds location 
        and can be fetched using the tuple containing 
        (record_id, location)
    '''

    def __init__(self):
        self.cds_repository = {}
        self.record_repository = RecordContainer.Instance()

    
    def populate (self, readCont):

        # Iterate through reads
        num = 0;
        for read in readCont.read_repository.values():

            # Iterate through read alignments
            for readAln in read.alignment_locations:
                num += 1;

                # Get CDSs for alignment



            

        print "pogledao sam alignova: %d " % num

        pass
