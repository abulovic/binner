# @author Martin Sosic (sosic.martin@gmail.com) & Matija Sosic (matija.sosic@gmail.com)
from utils.Location import Location

def num_reads(read_container):
    """
    @param (ReadContainer) read_container
    @return (int) Number of reads in read container.
    """
    return len(read_container.read_repository)

# Matija
def num_reads_with_no_alignments(read_container):
    ''' Counts reads that have no alignment.

        @param (ReadContainer) read_container   Holds reads
        @return Number of reads with 0 alignments
    '''
    no_align_num = 0
    for read in read_container.values():
        if not read.has_alignments():
            no_align_num += 1


    return no_align_num

# Cekati da Ana napravi podrsku
def num_reads_with_host_and_parasit_alignments():
    pass

# Martin
def num_reads_with_no_aligned_cdss(read_container, cds_aln_container):
    """
    @param (ReadContainer) read_container
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of reads that do not align to any cds.
    """
    num_reads_with_aligned_cdss = len([ls for ls in cds_aln_container.read2cds.values() if len(ls) > 0])
    return num_reads(read_container) - num_reads_with_aligned_cdss

# Martin
def num_reads_with_multiple_aligned_cdss(cds_aln_container):
    """
    @param (CdsAlnContainer) cds_aln_container
    @return (int) Number of reads that align to multiple(more than one) cdss.
    """
    return len([ls for ls in cds_aln_container.read2cds.values() if len(ls) > 1])

# Matija
def num_reads_with_multiple_mapped_cds_sublocations(read_container):
    ''' Counts reads that have alignment which intersects with multiple 
        sublocations of single CDS.

        @param (ReadContainer) read_container Read container
        @return Number of reads which satisfy the above written condiion
    '''

    ret = 0
    for read in read_container.values():
        count_this_read = False

        for aln in read.alignment_locations:
            for (cds, cds_location) in aln.aligned_cdss:
                if is_aln_mapped_to_multiple_cds_sublocs(aln, cds_location):
                    count_this_read = True

        if count_this_read:
            ret += 1

    return ret
            

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
            if aln.location_span.intersects(subloc):
                intersected_sublocs += 1

        return (intersected_sublocs > 1)
            





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

# Martin
def calc_average_cds_coverage(cds_aln_container):
    """ Calculates average cds coverage and standard deviation (uncorrected sample standard deviation).
    Cds coverage is average number of reads per base of cds.
    @param (CdsAlnContainer) cds_aln_container
    @return (float, float) (average, standard deviation)
    """
    # List of floats
    coverages = map(calc_cds_coverage, cds_aln_container.cds_repository.values())
    average = sum(coverages) / float(len(coverages))
    deviation = sqrt(sum([(c-average)**2 for c in coverages]) / float(len(coverages)))
    return (average, deviation)
    

