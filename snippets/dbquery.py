import sys, os
sys.path.append(os.getcwd())

from ncbi.db.access import DbQuery

def checkRecord(record_name):

    record = dbquery.get_record(record_name)

    if not record:
        print "record %s: Does not exist!" % record_name
    else:
        print "record %s: Exists!: %d" % (record.name, len(record.cdss))


if __name__ == '__main__':

	dbquery = DbQuery ()
	
	record_id = 'AB000181'
	location = (100,200)
	complement = True

        checkRecord("AB000181")
        checkRecord("Z46234")   # Exists
        checkRecord("M19921.2") # Does not exist

	# first way to get the cdss that queries
	# the record itself
	# cdss = record.find_cds(location, complement)
	# print "Found {0} cdss directly from record.".format(len(cdss))
	# second way to get the cdss that surpasses
	# the record query and need to store records
	# cdss = dbquery.get_cdss(record_id, location, complement)
	# print "Found {0} cdss using dbquery.".format(len(cdss))
