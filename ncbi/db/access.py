from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
import _mysql

import ncbi.db.genbank as gb
import ncbi.db.embl as embl

class DbQuery(object):
    '''Serves as a database query utility.'''
    def __init__(self, genbank_db_url=None, embl_db_url=None, ncbitax_db_url=None):
        if not genbank_db_url:
            genbank_db_url = "mysql+mysqldb://root:root@localhost/genbank"
        self.genbank_db_url = genbank_db_url
        if not embl_db_url:
            embl_db_url = "mysql+mysqldb://root:root@localhost/embl"
        self.embl_db_url = embl_db_url
        if not ncbitax_db_url:
            ncbitax_db_url = "mysql+mysqldb://root:root@localhost/ncbitax"
        self.ncbitax_db_url = ncbitax_db_url
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

    def get_taxids (self, gis, format=dict):
        '''
        Fetches taxonomy ID for each of the GIs.
        @param gis (list) list of integers representing GIs
        @param format (object type) list or dict.
        @return based on format parameter, returns either list of 
        tax IDs or a dictionary mapping gis to tax ids. List can 
        contain duplicates.
        '''
        if not gis:
            return format()
        sql_query = "SELECT * FROM gi_taxid_nuc WHERE gi IN %s" % ( '(' + str(gis)[1:-1] + ')' )
        self.ncbitax_db.query(sql_query)
        result = self.ncbitax_db.use_result()

        gi2taxid_list = result.fetch_row(maxrows=0)

        if format == dict:
            gi2taxid_dict = {}
            for (gi, taxid) in gi2taxid_list:
                gi2taxid_dict[int(gi)] = int(taxid)

            return gi2taxid_dict

        elif format == list:
            taxid_list = []
            for (gi, taxid) in gi2taxid_list:
                taxid_list.append (int(taxid))

            return taxid_list

        else:
            return None

    def get_organism_name (self, taxid, name_class='scientific name'):
        ''' 
        Fetches organism name for the speficied taxonomy ID.
        @param taxid (int)  taxonomy ID
        @param name_class (str) scientific name, common name, genbank common
        name, authority
        @return organism name (str)
        '''
        self.ncbitax_db.query('SELECT name_txt FROM ncbi_names WHERE tax_id=%d and name_class="%s"'
                                % (taxid, name_class))
        result = self.ncbitax_db.use_result()
        org_name = result.fetch_row()
        if org_name:
            ((org_name,),) = org_name
        return org_name


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

        self.ncbitax_db = _mysql.connect('localhost', 'root', 'root', 'ncbitax')

        
