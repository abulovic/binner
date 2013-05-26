'''
:Date: 12.05.2013.
:Author: Ana Bulovic <bulovic.ana@gmail.com>
'''

from data.read import Read
from utils.location import Location

import time

class ReadContainer (object):
    ''' 
    Contains all the reads (:class:`data.read.Read`) loaded from an alignment file. Can be queried by read id.
    The ReadContainer is populated in two stages.
    First, it loads all the information available from the alignment file::

        read_cont = ReadContainer()
        read_cont.populate_from_aln_file(aln_file)

    After that, it needs information from the database filled with NCBI sequences data. 
    :class:`data.containers.record.RecordContainer` serves as the interface to database, and 
    is used in the second stage of loading, where the coding sequence locations are loaded
    from the database::

        record_cont = RecordContainer()
        record_cont.set_db_access()
        read_cont.populate_cdss(read_cont)
    '''
    def __init__(self):
        """
        (dict) read_repository Dictionary where value is (Read)read and key is (str)read id.
        """
        self.read_repository = {}
        
    def populate_from_aln_file (self, read_alignment_file):
        ''' 
        Adds all the reads in the alignment file to the read repository.
        First stage read container populating.

        :param read_alignment_file: path to Binner input file (as specified in doc.format.specs)
        '''
        aln_file = open(read_alignment_file, 'r')
        for line in aln_file.readlines():
            self._add_read_from_str(line)

    def populate_cdss (self, record_container):
        '''
        Coding sequences are determined and stored for every read alignment using
        information from the record container.
        Prerequisite: record container has been populated with all records
        mentioned in the alignment file

        :param record_container: :class:`data.containers.record.RecordContainer` which has already been populated
        '''
        
        # -------------------------------- Sorting CDSs ---------------------------- #

        start = time.time()

        # Sort cdss of each record by start
        for record in record_container.record_repository.itervalues():
            if (not record):
                continue

            # Is this slow, calculating key each time?
            record.cdss.sort(key = lambda c : Location.from_location_str(c.location).start)

        end = time.time()
        elapsed_time = end - start
        print ("Sorting CDSs - elapsed time: %.2f" % elapsed_time)

        # ---------------------------------------------------------------------------- #

        start = time.time()

        for read in self.fetch_all_reads(format=iter):
            for read_alignment in read.get_alignments(format=iter):
                read_alignment.determine_coding_seqs_optimal(record_container)

        end = time.time()
        elapsed_time = end - start
        print ("Mapping aln -> [cds] - elapsed time: %.2f" % elapsed_time)

    
    def fetch_read (self, read_id):
        '''
        Fetch read (:class:`data.read.Read`) by read ID. Read ID is 
        loaded from the alignment file.

        :param read_id: Read ID, as stated in the alignment file
        :rtype: :class:`data.read.Read`
        '''
        if self.read_repository.has_key(read_id):
            return self.read_repository[read_id]
        else:
            raise KeyError("Read repository doesn't contain read associated with read ID: {0}".format(read_id))


    def fetch_all_reads (self, format=iter):
        '''
        Fetch all read objects (:class:`data.read.Read`) that have been stored in the container
        during the populate phase.

        :param format: format in which all the reads will be returned. All default python collection formats are allowed (list, set), including the iterator
        :rtype: format(list of Reads)
        '''
        return format(self.read_repository.values())
    
    def _add_read_from_str (self, read_str):
        read = Read.from_read_str(read_str)
        assert (not self.read_repository.has_key(read.id))
        self.read_repository[read.id] = read
        
