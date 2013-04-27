import db.access
import db.data

if __name__ == '__main__':

	dbquery = DbQuery ()
	
	record_id = 'AB000181'
	location = (100,200)
	complement = True

	record = dbquery.get_record(record_id)
	print record

	# first way to get the cdss that queries
	# the record itself
	cdss = record.find_cds(location, complement)
	print "Found {0} cdss directly from record.".format(len(cdss))
	# second way to get the cdss that surpasses
	# the record query and need to store records
	cdss = dbquery.get_cdss(record_id, location, complement)
	print "Found {0} cdss using dbquery.".format(len(cdss))
