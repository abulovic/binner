from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative.api import declarative_base, DeferredReflection

from ncbidb.data import Record

class DbQuery(object):
	'''Serves as a database query utility.'''
	def __init__(self, db_url=None):
		if not db_url:
			 db_url = "mysql+mysqldb://root@localhost/genome"
		self.db_url = db_url
		self._create_session()


	def get_record (self, record_id, db_source='gb'):
		''' 
		@param record_id GenBank/EMBL/DDBJ record ID
		@param db_source source database, can be gb(GenBank),
			   emb(EMBL), dbj(DDBJ)
		@return Record object with specified id,
				None if no object with that id is present in database
		'''
		r = session.query(Record).filter(Record.name=='AB000181').first()
		return r


	def get_cdss   (self, record_id, location, complement=False, db_source='gb'):
		''' 
		@param location location tuple (start, stop)
		@param complement True if cds is on the complementary strand
		@return List of Cds objects from the record specified
				by the record_id for the specified location
		'''
		pass

	def _create_session (self):
		''' Creates database session '''
		engine = create_engine (self.db_url, echo=False, 
								convert_unicode=True, encoding='utf-8')
		session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
		Base = declarative_base(cls=DeferredReflection)
		Base.prepare(engine)
		self.session = db.session()

		