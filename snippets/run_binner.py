import logging
import logging.config
import argparse
import sys,os
sys.path.append(os.getcwd())
from data.containers.read import ReadContainer
from data.containers.record import RecordContainer
from ncbi.db.access import DbQuery

from utils import timing

from solver.Solver import Solver
from solver.taxonomy.SimpleTaxonomySolver       import SimpleTaxonomySolver
from solver.taxonomy.SimpleJoinTaxonomySolver   import SimpleJoinTaxonomySolver
from solver.read2cds.GreedySolver               import GreedySolver
from solver.read2cds.BestScoreSolver            import BestScoreSolver
from solver.determine_host                      import determine_host

def parse_input_parameters():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Reads input and desscription files and prodices output '
        'file')
    argparser.add_argument('input', help='Input alignment file', 
                           type=str)
    argparser.add_argument('descr', help='XML description schema', 
                           type=str)
    argparser.add_argument('output', help='Output XML file', 
                           type=str)
    argparser.add_argument('-sd', '--stats_dir', 
                           help='Statistics output directory. ' +
                           'Will be created if it does not exit.',
                           type=str, default=None)
    argparser.add_argument('-sf', '--solution_file', 
                           help='Xml solution file. If specified, comparison ' +
                           'of solver phases and solution will be done.',
                           type=str, default=None)
    argparser.add_argument('-ts', '--tax_solver', 
                           help='Taxonomy solver type', 
                           choices=['simple', 'simple_join'], 
                           default='simple')
    argparser.add_argument('-rs', '--read2cds_solver', 
                           help='Read2CDS solver type', 
                           choices=['greedy', 'best_score'], 
                           default='greedy')
    argparser.add_argument('-l', '--log_configuration',
                           help='Logging configuration file', type=str,
                           default='config' + os.path.sep + 'logging.ini')
    mutexgroup = argparser.add_mutually_exclusive_group()
    mutexgroup.add_argument('--cds-db-connection', 
        default='mysql+mysqldb://root:root@localhost/unity',
        help='CDS database connection string')
    mutexgroup.add_argument('--cds-fasta',
        help='CDS fasta file location')
    argparser.add_argument('--ncbitax-db-connection', 
       default='mysql+mysqldb://root:root@localhost/ncbitax',
        help='NCBI Taxonomy database connection string')
    argparser.add_argument('-tt', '--tax-tree', 
       help='Taxonomy tree location', 
       default='./ncbi/taxonomy/.data/ncbi_tax_tree')

    args = argparser.parse_args()
    
    error = False
    if not os.path.exists(os.path.expanduser(args.input)):
        print "Input alignment file %s doesn't exist" % args.input
        error = True
    if not os.path.exists(os.path.expanduser(args.descr)):
        print "XML description schema %s doesn't exist" % args.descr
        error = True
    if not os.path.exists(os.path.expanduser(args.log_configuration)):
        print "Log configuration file %s doesn't exist" % args.log_configuration
        error = True
    if args.cds_fasta is not None:
        if not os.path.exists(os.path.expanduser(args.cds_fasta)):
            print "CDS Fasta file %s doesn't exists" % args.descrargs.cds_fasta
    if error:
        exit(-1)
    
    print args
    exit(1)
    return args

if __name__ == '__main__':
    log = logging.getLogger(__name__)

    args = parse_input_parameters()

    # load the logging configuration
    logging.config.fileConfig(args.log_configuration,
                              disable_existing_loggers=False)

    log.info('BINNER RUN')
    log.info("Input: %s" % args.input)
    log.info("Xml template: %s" % args.descr)
    log.info("Output: %s" %  args.output)
    
    
    read2cds_solver = None
    log.info("read2cds solver: %s" % args.read2cds_solver)
    if args.read2cds_solver == 'greedy':
        read2cds_solver = GreedySolver()
    elif args.read2cds_solver == 'best_score':
        read2cds_solver = BestScoreSolver()
    
    tax_solver = None
    log.info("taxonomy solver: %s" % args.tax_solver)
    if args.tax_solver == 'simple':
        tax_solver = SimpleTaxonomySolver()
    elif args.tax_solver == 'simple_join':
        tax_solver = SimpleJoinTaxonomySolver()
    
    log.info("Started.")
    processing_start = timing.start()
    
    solver = Solver(determine_host, read2cds_solver, tax_solver)

    # Populate read container
    # The read container type can now be determined from the input parameters
    # and injected into the Solver
    start = timing.start()
    read_container = ReadContainer()
    read_container.populate_from_aln_file(read_alignment_file=args.input)
    elapsed_time = timing.end(start)
    log.info("Populate read container - elapsed time: %s", 
             timing.humanize(elapsed_time))    
    
    # Create database access
    db_access = DbQuery()
        
    # Populate record container
    # The record container type can now be determine from the input parameters
    # and injected into the Solver
    start = timing.start()
    record_container = RecordContainer()
    record_container.set_db_access(db_access)
    # Extract all records from database
    record_container.populate(read_container.fetch_all_reads_versions())
    elapsed_time = timing.end(start)
    log.info("Populate record container - elapsed time: %s", 
             timing.humanize(elapsed_time)) 
   
    solver.generateSolutionXML(read_container=read_container,
                               record_container=record_container,
                               dataset_xml_file=args.descr,
                               output_solution_filename=args.output,
                               stats_dir=args.stats_dir,
                               solution_file=args.solution_file)
    
    processing_delta = timing.end(processing_start)
    log.info("Processing done in %s", 
        timing.humanize(processing_delta))
    
    log.info("Finished.")
