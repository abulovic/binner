# @author Martin Sosic (sosic.martin@gmail.com) & Matija Sosic (matija.sosic@gmail.com)
from utils.Location import Location

def num_reads(read_container):
    """
    @param (ReadContainer) read_container
    @return (int) Number of reads in read container.
    """
    return len(read_container.read_repository)

# Matija
def num_reads_with_no_alignments():
    pass

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
def num_reads_with_multiple_mapped_cds_sublocations():
    pass

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
    

