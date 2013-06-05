# -*- coding: utf-8 -*-
'''
Created on May 19, 2013

@author: marin
'''
import os
import sys
import logging
import argparse
# import sh
# from util import timing
from fastacds import FastaCDS
from parser.unity import UnityCDS, UnityRecord
import traceback

#set log
log = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch) 
log.setLevel(logging.DEBUG)

unity_mem = {}

def to_unity_cds(record):
    attributes = {
        intern('nucl_gi') : record.nucl_gi,
        intern('db') : record.db,
        intern('version') : record.version,
        intern('cds') : record.cds,
        intern('location') : record.location,
        intern('origin') : record.origin,
        intern('taxon') : record.taxon[0] if record.taxon else None,
        intern('protein_id') : record.protein_id[0] if record.protein_id else None,
        intern('locus_tag') : record.locus_tag[0] if record.locus_tag else None,
        intern('product') : record.product[0] if record.product else None,
        intern('gene') : record.gene[0] if record.gene else None,
        intern('prot_gi') : record.prot_gi[0] if record.prot_gi else None
    }
    return UnityCDS(attributes)

def add_cds(cds):
    record = unity_mem.get(cds.version)
    if not record:
        record = UnityRecord(cds.version)
        unity_mem[record.version] = record
    
    record.add_cds(cds)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Parses the input Fasta file and loads it into memory. '
        'After the process is finished the memory usage is reported.' )
    argparser.add_argument('input_file', 
        help='Fasta file to analyze')

    args=argparser.parse_args()
    
    error = False
    if not os.path.exists(os.path.expanduser(args.input_file)):
        print "File %s doesn't exist" % args.input_file
        error = True

    if error:
        exit(-1)

    processing_start = timing.start()
    
    input_file = os.path.expanduser(args.input_file)

    log.info('Processing file %s', args.input_file)
        
    fc = FastaCDS(input_file)

    count = 0
    for record in fc.parse():
        try:
            cds = to_unity_cds(record)
            add_cds(cds)
            count += 1
        except Exception as e:
            log.error(traceback.format_exc())
            log.warn('Record %s skipped', record.version)

    
    log.info('%d records successfully loaded', count)
    
    processing_delta = timing.end(processing_start)
    log.info("File %s loaded into memory in %s", 
        args.input_file, timing.humanize(processing_delta))
    
    # mem_usage = float(sh.awk(sh.ps('u','-p',os.getpid()),
                             #'{sum=sum+$6}; END {print sum/1024}'))
    
    log.info("Memory usage %.1fMiB", mem_usage)

