from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm             import relationship
from sqlalchemy.schema          import Column, ForeignKey
from sqlalchemy.types           import BigInteger

from utils.location             import Location

Base = declarative_base(cls=DeferredReflection)
class Record(Base):
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