from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
import _mysql

from ncbi.db.unity import UnityRecord, UnityCDS

class DbQuery(object):
    '''Serves as a database query utility.'''
    def __init__(self, unity_db_url=None, ncbitax_db_url=None):
        if not unity_db_url:
            unity_db_url = "mysql+mysqldb://root:root@localhost/unity"
        self.unity_db_url = unity_db_url
        if not ncbitax_db_url:
            ncbitax_db_url = "mysql+mysqldb://root:root@localhost/ncbitax"
        self.ncbitax_db_url = ncbitax_db_url
        self._create_sessions()


    def get_record (self, version):
        ''' 
        @param record_id GenBank/EMBL/DDBJ/RefSeq Accesion.Version
        @return Record object with specified id,
                None if no object with that id is present in database
        '''
        records = self.unity_session.execute("""
        
            SELECT id, db, version, nucl_gi, taxon, location,
                protein_id, locus_tag, product, gene, prot_gi
            FROM cds
            WHERE version LIKE :version;
        """,
        {
            'version': version
         })

        record = None

        for r in records:
            if not record:
                record = UnityRecord(r['version'])
            cds = UnityCDS(dict(r))
            record.add_cds(cds)
    
        return record
        

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

    def get_organism_rank (self, query, by_name=False):
        '''
        Fetches organism rank. Query can be done using organism name 
        or organism tax ID. 
        @param query (str/int) depends on by_name parameter
        @param by_name (boolean) true if query should be done using organism
        name instead of tax ID.
        @return (str) organism taxonomy rank
        '''
        if by_name:
            tax_id = self.get_organism_taxid(query)
        else:
            tax_id = query
        if not tax_id:
            return None

        tax_id = int(tax_id)
        sql = 'SELECT rank FROM ncbi_nodes WHERE tax_id=%d'
        self.ncbitax_db.query(sql % tax_id)
        result = self.ncbitax_db.use_result()
        rank = result.fetch_row()
        if rank:
            ((rank,),) = rank
        return rank

    def get_organism_taxid (self, organism_name, name_class='scientific name'):
        '''
        Fetches organism taxid for the specified organism name.
        @param organism_name (str) organism nam
        @return taxid (int)
        '''
        sql = 'SELECT tax_id FROM ncbi_names WHERE name_class="%s" AND name_txt="%s"'
        self.ncbitax_db.query (sql % (name_class, organism_name))
        result = self.ncbitax_db.use_result()
        tax_id = result.fetch_row()
        if tax_id:
            ((tax_id,),) = tax_id
            tax_id = int(tax_id)
        return tax_id


    def _create_sessions(self):
        ''' Creates database sessions '''
        unity_engine = create_engine (self.unity_db_url, echo=False, 
                                convert_unicode=True, encoding='utf-8')
        unity_session = scoped_session(sessionmaker(
                        bind=unity_engine, autocommit=False, autoflush=False))
        
        self.unity_session = unity_session()

        self.ncbitax_db = _mysql.connect('localhost', 'root', 'root', 'ncbitax')

        
