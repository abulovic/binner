Data objects
************

There are two type of objects in the Binner.
First type are the alignment - related objects, and they are all
container within the data module. 

The other type is the NCBI record data, which can be found 
in the :module:`ncbi.db.genbank` and :module:`ncbi.db.embl` modules.

------------
Read object
------------
.. automodule:: data.read
.. autoclass:: Read
    :members:

-------------------------
Alignment related objects
-------------------------
.. automodule:: data.alignment
.. autoclass:: CdsAlignment
    :members:
.. autoclass:: CdsAlnSublocation
    :members:
.. autoclass:: ReadAlnLocation
    :members:
