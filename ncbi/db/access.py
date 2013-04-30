from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

import ncbi.db.genbank as gb
import ncbi.db.embl as embl

class DbQuery(object):
    '''Serves as a database query utility.'''
    def __init__(self, genbank_db_url=None, embl_db_url=None):
        if not genbank_db_url:
            genbank_db_url = "mysql+mysqldb://root:root@localhost/genbank"
        self.genbank_db_url = genbank_db_url
        if not embl_db_url:
            embl_db_url = "mysql+mysqldb://root:root@localhost/embl"
        self.embl_db_url = embl_db_url
        self._create_sessions()


    def get_record (self, record_id, db_source='gb'):
        ''' 
        @param record_id GenBank/EMBL/DDBJ record ID
        @param db_source source database, can be gb(GenBank),
               emb(EMBL), dbj(DDBJ)
        @return Record object with specified id,
                None if no object with that id is present in database
        '''
        if db_source == 'gb':
            result = self.genbank_session.query(gb.Record).filter(gb.Record.name==record_id).first()
        elif db_source == 'embl':
            result = self.embl_session.query(embl.Record).filter(embl.Record.name==record_id).first()
        else:
            raise ValueError('db_source: %s not supported', str(db_source))

        return result


    def get_cdss   (self, record_id, location, complement=False, db_source='gb'):
        ''' 
        @param location location tuple (start, stop)
        @param complement True if cds is on the complementary strand
        @return List of Cds objects from the record specified
                by the record_id for the specified location
        '''
        record = self.get_record(record_id, db_source)
        if record:
            return record.matches(location, complement)
        else:
            return []

    def _create_sessions(self):
        ''' Creates database sessions '''
        genbank_engine = create_engine (self.genbank_db_url, echo=False, 
                                convert_unicode=True, encoding='utf-8')
        genbank_session = scoped_session(sessionmaker(bind = genbank_engine, autocommit=False, autoflush=False))
        
        gb.init_db(genbank_engine)
        self.genbank_session = genbank_session()
        
        embl_engine = create_engine (self.embl_db_url, echo=False, 
                                convert_unicode=True, encoding='utf-8')
        embl_session = scoped_session(sessionmaker(bind = embl_engine, autocommit=False, autoflush=False))
        
        embl.init_db(embl_engine)
        self.embl_session = embl_session()

        
