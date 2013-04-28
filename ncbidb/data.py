from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm             import relationship
from sqlalchemy.schema          import Column, ForeignKey
from sqlalchemy.types           import BigInteger

from utils.location             import Location

Base = declarative_base(cls=DeferredReflection)
class Record(Base):
    ''' Attributes:
        accession:  nucleotide accession
        cdss:       list of coding sequences in the record
        gi:         genome index
        name:       same as accession? 
        version:    contains accession.version (example AB000181.1)
    '''
    __tablename__ = 'record'
    
    def find_cds(self, location, complement=False, tolerance=0):
        results = []
        for cds in self.cdss:
            if cds.matches(location, complement, tolerance):
                results.append(cds)
        return results

    def __str__(self):
        ''' Prints a record in human readable fashion. '''
        pass


    
class Cds(Base):
    ''' db_xref:    GI:genome_index (string)
        gene:       gene name
        id:         database id
        location:   location string (can be parsed with Location.from_location_str)
        locus_tag:  locus tag
        product:    protein product
        record:     record object (which contains this cds)
        record_id:  record id
    '''
    __tablename__ = 'cds'
    
    record_id = Column(BigInteger, ForeignKey('record.id'))
    
    record = relationship(
        Record,
        primaryjoin='Cds.record_id==Record.id',
        backref='cdss'
    )


    
    def matches(self, location, complement, tolerance):
        l1 = Location.from_location_str(self.location, tolerance)
        return l1.intersects(Location.from_location(location, complement))
    

class Source(Base):
    __tablename__ = 'source'
    
    record_id = Column(BigInteger, ForeignKey('record.id'))
    
    record = relationship(
        Record,
        primaryjoin='Source.record_id==Record.id',
        backref='sources'
    )
    
def init_db(engine):
    session.configure(bind=engine)
    Base.prepare(engine)