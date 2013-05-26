I/O Format specification
************************

Input file:
<read_id><n>;<nucl_acc>,<db_source>,<gi>,<score>,<start>,<stop>,<strand>;{n}

* read_id:      identification assiged to read from sequencing machine
* n:            number of significant alignments
* nucl_acc:     nucleotide accession of the sequence from NCBI NT database
* db_source:    database source (gb(GenBank), emb(EMBL), dbj(DNA Database of Japan))
* gi:           gene info ID (http://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html#GInB)
* score:        score that the aligner tool has determined for this alignment
* start:        staring location of the alignment on the nucleotide chain
* stop:         end location
* strand:       +/- strand of the nucleotide chain
