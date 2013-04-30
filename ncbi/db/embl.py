# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2013

@author: marin
'''
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger
from utils.location import Location

session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base(cls=DeferredReflection)

class Record(Base):
    ''' Attributes:
        accession:  nucleotide accession
        cdss:       list of coding sequences in the record
        sources:    list of source elemtns in the record
        gi:         genome index - always None
        name:       same as accession? 
       version:    contains accession.version (example AB000181.1)
    '''
    __tablename__ = 'record'
    gi = None
    
    def find_cds(self, location, complement=False, tolerance=0):
        results = []
        for cds in self.cdss:
            if cds.matches(location, complement, tolerance):
                results.append(cds)
        return results
    
class Cds(Base):
    ''' db_xref:    GI:genome_index (string) 
        gene:       gene name
        id:         database id
        location:   location string (can be parsed with Location.from_location_str)
        locus_tag:  locus tag
        product:    protein product
        record:     record object (which contains this cds)
        record_id:  record id
        additional_db_xrefs:    additional db_xref identifiers (list of objects)
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
    
class CdsAdditionalDbXref(Base):
    ''' cds:        crd reference
        cds_id:     cds id
        db_xref:    additional reference (string)
    '''
    __tablename__ = 'additional_cds_db_xref'
    
    cds_id = Column(BigInteger, ForeignKey('cds.id'))
    
    cds = relationship(
        Cds,
        primaryjoin='CdsAdditionalDbXref.cds_id==Cds.id',
        backref='additional_db_xrefs'
    )

class Source(Base):
    ''' db_xref:    taxon:number (string)
        id:         database id
        location:   location string (can be parsed with Location.from_location_str)
        organism:    protein product
        record:     record object (which contains this cds)
        record_id:  record id
        additional_db_xrefs:    additional db_xref identifiers (list of objects)
    '''
    __tablename__ = 'source'
    
    record_id = Column(BigInteger, ForeignKey('record.id'))
    
    record = relationship(
        Record,
        primaryjoin='Source.record_id==Record.id',
        backref='sources'
    )
    
class SourceAdditionalDbXref(Base):
    ''' source:        source reference
        cource_id:     source id
        db_xref:       additional reference (string)
    '''
    __tablename__ = 'additional_source_db_xref'
    
    source_id = Column(BigInteger, ForeignKey('source.id'))
    
    source = relationship(
        Source,
        primaryjoin='SourceAdditionalDbXref.source_id==Source.id',
        backref='additional_db_xrefs'
    )
    
    
def init_db(engine):
    session.configure(bind=engine)
    Base.prepare(engine)
