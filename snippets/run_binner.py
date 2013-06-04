import logging
import logging.config
import argparse
import sys,os
sys.path.append(os.getcwd())

from utils import timing

from solver.Solver import Solver
from solver.taxonomy.SimpleTaxonomySolver       import SimpleTaxonomySolver
from solver.taxonomy.SimpleJoinTaxonomySolver   import SimpleJoinTaxonomySolver
from solver.read2cds.GreedySolver               import GreedySolver
from solver.read2cds.BestScoreSolver            import BestScoreSolver
from solver.determine_host                      import determine_host

if __name__ == '__main__':
    log = logging.getLogger(__name__)

    argparser = argparse.ArgumentParser(
        description='Reads input and desscription files and prodices output '
        'file')
    argparser.add_argument('input', help='Input alignment file', 
                           type=str)
    argparser.add_argument('descr', help='XML description schema', 
                           type=str)
    argparser.add_argument('output', help='Output XML file', 
                           type=str)
    argparser.add_argument('stats_out_dir', help='Statistics output directory. '+
                           'Will be created if it does not exist.',
                           type=str)
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
    if error:
        exit(-1)

    # load the logging configuration
    logging.config.fileConfig(args.log_configuration,
                              disable_existing_loggers=False)

    log.info('BINNER RUN')
    log.info("Input: %s" % args.input)
    log.info("Xml template: %s" % args.descr)
    log.info("Output: %s" %  args.output)
    log.info("Statistics output directory: %s" % args.stats_out_dir)
    
    
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
    solver.generateSolutionXML(args.input, args.descr, args.output, args.stats_out_dir)
    
    processing_delta = timing.end(processing_start)
    log.info("Processing done in %s", 
        timing.humanize(processing_delta))
    
    log.info("Finished.")
