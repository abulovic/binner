Data Containers
***************
Containers are helper objects that serve as custom collections 
for data objects. They all implement methods for self-populating, and
fetching their stored items.

They are usually used together::

    read_cont   = ReadContainer()
    record_cont = RecordContainer()
    record_cont.set_db_access(db_access)
    cdsaln_cont = CdsAlnContainer()

    # 1. Load all the information available in the alignment file
    read_cont.populate_from_aln_file(alignment_file)
    # 2. Fetch all the records reported in the alignment file from the database
    record_cont.populate(read_cont)
    # 3. Find to which coding sequences reads map
    read_cont.populate_cdss(record_cont)
    # 4. Populate Cds Alignment container
    cdsaln_cont.populate(read_cont)

=================
Container classes
=================
-------------
ReadContainer
-------------
.. automodule:: data.containers.read
.. autoclass:: ReadContainer
    :members:

---------------
CdsAlnContainer
---------------
.. automodule:: data.containers.cdsaln
.. autoclass:: CdsAlnContainer
    :members:

---------------
RecordContainer
---------------
.. automodule:: data.containers.record
.. autoclass:: RecordContainer
    :members:
    
---------------
Loading methods
---------------
.. automodule:: data.containers.load
.. autofunction:: fill_containers
