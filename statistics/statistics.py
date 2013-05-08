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
def num_reads_with_no_aligned_cdss():
    pass

# Martin
def num_reads_with_multiple_aligned_cdss():
    pass

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
            





# Matija
def average_cds_coverage():
    pass
