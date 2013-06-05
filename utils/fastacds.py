# -*- coding: utf-8 -*-
'''
Created on May 18, 2013

@author: marin
'''
import os
import gzip
import re
import textwrap

database_fields =[
    'gb',
    'emb',
    'ref',
    'dbj'
]
standard_fields =[
    'nucl_gi',
    'taxon',
    'location',
    'protein_id',
    'locus_tag',
    'product',
    'gene',
    'prot_gi',
    'cds'
]

splitter_regex = ('(' + 
    '|'.join(['>' + dbf + '\|' for dbf in database_fields]) +
    '|' +
    '|'.join(['\|' + sf + '\|' for sf in standard_fields]) + ')')

class FastaCDSRecord(object):
    def __init__(self, db, version, nucl_gi, location, cds, attributes={}):
        self.nucl_gi = nucl_gi
        self.db = db
        self.version = version
        self.cds = cds
        self.location = location
        self.attributes = attributes
        self.origin = None
        
    def __getattr__(self, name):
        if self.attributes.has_key(name):
            return self.attributes[name]
        elif name in standard_fields:
            return []
        else:
            raise AttributeError("'%s' object has no attribute '%s'",
                self.__class__.__name__, name)
    
    def lines(self):
        line_info = []
        line_info.append('>')
        line_info.append(self.db)
        line_info.append('|')
        line_info.append(self.version)
    
        if self.nucl_gi:
            line_info.append('|nucl_gi|')
            line_info.append(self.nucl_gi)
                
        
        for tax in self.taxon:
            line_info.append('|taxon|')
            line_info.append(tax)
        
        line_info.append('|location|')
        line_info.append(self.location)
        
        for protein_id in self.protein_id:
            line_info.append('|protein_id|')
            line_info.append(protein_id)
        
        for locus_tag in self.locus_tag:
            line_info.append('|locus_tag|')
            line_info.append(locus_tag)
            
        for product in self.product:
            line_info.append('|product|')
            line_info.append(product)
        
        for gene in self.gene:
            line_info.append('|gene|')
            line_info.append(gene)
    
        for prot_gi in self.prot_gi:
            line_info.append('|prot_gi|')
            line_info.append(prot_gi)
        
        line_info.append('|cds|')
        line_info.append(self.cds)
        yield ''.join(line_info)
        yield '\n'
        
        if self.origin:
            yield self.origin
            yield '\n'

    
    @classmethod
    def parse_record(cls, lines):
        first_line = lines[0].strip()
        origin_lines = lines[1:]
        header = re.split(splitter_regex, first_line)[1:]
        db = header[0][1:-1]
        version = header[1]
        nucl_gi = header[3]
        cds = header[-1]
        rest = header[4:-2]
        attributes = {}
        location = None
        for k, v in zip(rest, rest[1:])[::2]:
            k = k[1:-1]
            if k == 'location':
                location = v
            else:
                if not attributes.has_key(k):
                    attributes[k] = []
                attributes[k].append(v)
                
        record = FastaCDSRecord(db, version, nucl_gi, location, cds, attributes)
        record.origin = ''.join([l.strip() for l in origin_lines])
        
        return record
        
class FastaCDS(object):
    def __init__(self,file_name):
        if not os.path.exists(file_name):
            raise IOError("File %s doesn't exist" % file_name)
        self.file_name = file_name
        
    def parse(self):
        _open = open
        if self.file_name.endswith('.gz'):
            _open = gzip.open
        
        with _open(self.file_name, "rt") as f:
            record_lines = []
            while True:
                line = f.readline()
                if line.startswith('>') or not line:
                    if record_lines:
                        record = FastaCDSRecord.parse_record(record_lines)
                        if record:
                            yield record
                    if not line:
                        break
                    record_lines = [line]
                else:
                    record_lines.append(line)

