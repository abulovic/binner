# -*- coding: utf-8 -*-
'''
Created on May 27, 2013

@author: marin
'''
import sys
from utils.location import Location

class UnityRecord(object):
    def __init__(self, version):
        self.version = version
        self.cds = []
    
    def add_cds(self, cds):
        self.cds.append(cds)

class UnityCDS(object):
    __slots__ =  (
        'id',
        'db',
        'version',
        'nucl_gi',
        'taxon',
        'location',
        'protein_id',
        'locus_tag',
        'product',
        'gene',
        'prot_gi',
        'cds',
        'origin',
        'record_id', #compatibility issue
        'location_min' #optimization issue        
    )
    
    def __init__(self, attributes={}):
        self.origin = None
        self.id = attributes.get('id')
        self.db = attributes.get('db')
        self.version = attributes.get('version')
        self.nucl_gi = attributes.get('nucl_gi')
        self.taxon = attributes.get('taxon')
        self.location = attributes.get('location')
        self.protein_id = attributes.get('protein_id')
        self.locus_tag = attributes.get('locus_tag')
        self.product = attributes.get('product')
        self.gene = attributes.get('gene')
        self.prot_gi = attributes.get('prot_gi')
        self.cds = attributes.get('cds')
        self.record_id = self.version #Added because of compatibility with older code
                
        if self.location:
            self.location_min = Location.fast_min_str(self.location)
        else:
            self.location_min = sys.maxint

