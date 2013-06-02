# @author Martin Sosic (sosic.martin@gmail.com) & Matija Sosic (matija.sosic@gmail.com)
import math
from utils.location import Location

def num_reads(read_container):
    """
    @param (ReadContainer) read_container
    @return (int) Number of reads in read container.
    """
    return len(read_container.read_repository)


def num_reads_with_no_alns(read_container):
    ''' Counts reads that have no alignments.

        @param (ReadContainer) read_container   Holds reads
        @return Number of reads with 0 alignments
    '''
    no_align_num = 0
    for read in read_container.read_repository.values():
        if not read.has_alignments():
            no_align_num += 1


    return no_align_num


def num_reads_with_host_and_parasit_alignments(cds_aln_container):
    num_reads = 0
    for (read_id, cds_alns) in cds_aln_container.read2cds.items(): # for each read get cds_alns
        has_host_aln = False
        has_nonhost_aln = False # nonhost == parasit alignment
        for cds_aln in cds_alns:
            if cds_aln.aligned_regions[read_id].is_potential_host(): has_host_aln = True
            else: has_nonhost_aln = True
        if (has_host_aln and has_nonhost_aln):
            num_reads += 1
    return num_reads


def num_read_alns(read_container):
    """
    @param (ReadContainer) read_container
    @return (int) Number of read alignments.
    """
    num_alignments = 0
    for read in read_container.read_repository.values():
        num_alignments += len(read.alignment_locations)
    return num_alignments


def num_inactive_read_alns(read_container):
    """
    @param (ReadContainer) read_container
    @return (int) Number of read alignments that are not active.
    """
    num_inactive_alns = 0
    for read in read_container.read_repository.values():
        for aln in read.alignment_locations:
            if not aln.active:
                num_inactive_alns += 1
    return num_inactive_alns
    

def num_reads_with_no_aligned_cdss(read_container, cds_aln_container):
    """
    @param (ReadContainer) read_container
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of reads that do not align to any cds.
    """
    num_reads_with_aligned_cdss = len([ls for ls in cds_aln_container.read2cds.values() if len(ls) > 0])
    return num_reads(read_container) - num_reads_with_aligned_cdss


def num_reads_with_multiple_aligned_cdss(cds_aln_container):
    """
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of reads that align to multiple(more than one) cdss.
    """
    return len([ls for ls in cds_aln_container.read2cds.values() if len(ls) > 1])



def num_reads_with_multiple_mapped_cds_sublocations(read_container):
    ''' Counts reads that have alignment which intersects with multiple 
        sublocations of single CDS.

        @param (ReadContainer) read_container Read container
        @return Number of reads which satisfy the above written condiion
    '''

    # Function definitions ----------------------------------------------- #

    def tuple_intersects(t1, t2):
        return not (t1[0] > t2[1] or t2[0] > t1[1])

    def is_aln_mapped_to_multiple_cds_sublocs(aln, cds_location):
        ''' Returns true if read alignment intersects with multiple sublocations
            of given cds location

            Note: Should be called for CDSs that are on the nucl. chain of aln

            @param (ReadAln) aln            Read alignment
            @param (Location) cds_location  Location of CDS
            @return True if intersects with multiple sublocs of cds
        '''
        intersected_sublocs = 0
        for subloc in cds_location.sublocations:

            if tuple_intersects(aln.location_span, subloc):
                intersected_sublocs += 1

        return (intersected_sublocs > 1)

    # -------------------------------------------------------------------- #

    ret = 0
    for read in read_container.read_repository.values():
        count_this_read = False

        for aln in read.alignment_locations:
            for (cds, cds_location) in aln.aligned_cdss:
                if is_aln_mapped_to_multiple_cds_sublocs(aln, cds_location):
                    count_this_read = True

        if count_this_read:
            ret += 1

    return ret
            

def num_active_aligned_regions(cds_aln_container):
    """ 
    @param (CdsAlnContainer) cds_aln_container.
    @return (int) Number of active alignments (aligned regions). 
    At the beginning all alns are active.
    After determineHost() host alns are deactivated.
    After read2cdsSolver, alns with no mapping are deactivated. 
    """
    num_act_alns = 0
    for cds_aln in cds_aln_container.cds_repository.values():
        for aln_reg in cds_aln.aligned_regions.values():
            if aln_reg.active:
                num_act_alns += 1
    return num_act_alns
            


def calc_cds_coverage(cds_aln):
    """ Calculates coverage of cds.
    Coverage is average number of reads per base of cds.
    @param (CdsAlignment) cds_aln
    @return (float) Cds coverage.
    """
    coverage = 0
    for aln_reg in cds_aln.aligned_regions.values(): # aln_reg is of type CdsAlnSublocation
        location = aln_reg.location # location is of type Location
        coverage += location.length()
    coverage = coverage / float(Location.from_location_str(cds_aln.cds.location).length())
    return coverage


def calc_average_cds_coverage(cds_aln_container):
    """ Calculates average and standard deviation (uncorrected sample standard deviation) of cds coverage.
    Average is calculated for cdss that have at least one read aligned onto them.
    Cds coverage is average number of reads per base of cds.
    @param (CdsAlnContainer) cds_aln_container
    @return (float, float) (average, standard deviation)
    """
    # List of floats
    coverages = map(calc_cds_coverage, cds_aln_container.cds_repository.values())
    if (len(coverages) == 0): # this should never happen in real example
        return (float('NaN'), float('NaN'))
    average = sum(coverages) / float(len(coverages))
    deviation = math.sqrt(sum([(c-average)**2 for c in coverages]) / float(len(coverages)))
    return (average, deviation)
    


def num_cdss(cds_aln_container):
    """
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of cdss in cds_aln_container.
    """
    return len(cds_aln_container.cds_repository)


def num_cdss_with_no_alns(cds_aln_container):
    """
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of cdss in cds_aln_container with no active aligned regions.
    """
    num_cds = 0
    for cds_aln in cds_aln_container.cds_repository.values():
        is_empty = True
        for aln_reg in cds_aln.aligned_regions.values():
            if aln_reg.active:
                is_empty = False
        if is_empty:
            num_cds += 1
    return num_cds
        


class RecordStats (object):
    ''' Holds data for the record:
            record_id
            aln_count
            {cds_id: cds_aln_count}
    '''
    def __init__(self, record_id):
        self.record_id = record_id
        self.aln_count = 0
        self.cdss = {}

    def inc_aln_count(self):
        self.aln_count += 1
        
    def inc_aln_count_for_cds(self, cds_id):
        if cds_id not in self.cdss:
            self.cdss[cds_id] = 0
        self.cdss[cds_id] += 1

    def print_data(self):
        print "%s : %d" % (self.record_id, self.aln_count)
        for cds_id, aln_num in self.cdss.items():
            print "%s : %d\n" % (cds_id, aln_num)
        
    def __str__(self):
        ret = ""
        tab = " "*4
        ret += self.record_id + " : " + str(self.aln_count) + "\n"
        for cds_id, aln_num in self.cdss.items():
            ret += tab + str(cds_id) + " : " + str(aln_num) + "\n"

        return ret

def count_alns_to_record_and_cds(read_container):
    ''' For each record is counted  how much alignments aligned to it.
        Also, for each CDS in a record is counted the same thing.

        @param (ReadContainer) read_container
        @return {record_id : RecordStats }
    '''
    records_stats = {}

    for read in read_container.read_repository.values():
        for read_aln in read.alignment_locations:
            record_id = read_aln.nucleotide_accession

            # If not already in dict, create new object
            if record_id not in records_stats:
                records_stats[record_id] = RecordStats(record_id)

            records_stats[record_id].inc_aln_count()

            # Go through all CDSs of aln
            for (cds, loc) in read_aln.aligned_cdss:
                records_stats[record_id].inc_aln_count_for_cds(cds.version)
                
    return records_stats






    







