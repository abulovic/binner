from utils.singleton import Singleton

@Singleton
class RecordContainer (object):
    ''' Serves as a local Record Repository.
        If a GenBank/EMBL/DDBJ record has already been 
        fetched from the database, it can be fetched localy
        from the record repository.
    '''
    def __init__ (self):
        self.record_repository  = {}
        
    def set_db_access(self, db_query):
        self.db_query = db_query

    def fetch_record (self, record_id):
        self._add_record(record_id)
        return self.record_repository[record_id]
        
    def _add_record (self, record_id):
        ''' Adds the record from database if not already present
	   If unable to find entry in database, stores None instead.
        '''
        name = record_id.split('.')[0]
        if not self.record_repository.has_key(record_id):
	    record = self.db_query.get_record(name)
	    try :
    		getattr(record, 'name')
    		self.record_repository[record_id] = record

                print "Uspio, imam: ", record_id
	    except AttributeError:
    		print "No record with ID {0}".format(record_id)
    		self.record_repository[record_id] = None
