import argparse
import sys,os
sys.path.append(os.getcwd())

from solver.Solver import Solver
from solver.taxonomy.SimpleTaxonomySolver       import SimpleTaxonomySolver
from solver.taxonomy.SimpleJoinTaxonomySolver   import SimpleJoinTaxonomySolver
from solver.read2cds.GreedySolver               import GreedySolver
from solver.read2cds.BestScoreSolver            import BestScoreSolver
from solver.determine_host                      import determine_host

from utils.logger import Logger


argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='Input alignment file', type=str, nargs=1, dest='input')
argparser.add_argument('-d', '--descr', help='XML description schema', type=str, nargs=1, dest='descr')
argparser.add_argument('-o', '--out', help='Output XML file', type=str, nargs=1, dest='output')
argparser.add_argument('-ts', '--tax_solver', help='Taxonomy solver type', choices=['simple', 'simple_join'], default='simple', nargs=1, dest='tax_solver')
argparser.add_argument('-rs', '--read2cds_solver', help='Read2CDS solver type', choices=['greedy', 'best_score'], default='greedy', nargs=1, dest='read2cds_solver')
argparser.add_argument('-l', '--log', type=str, help='Path to log file', nargs=1, dest='log', default='binner.log')

args = argparser.parse_args()
print args

Logger(args.log)
log.info('BINNER RUN')
log.info("Input: %s" % args.input[0])
log.info("Xml template: %s" % args.descr[0])
log.info("Output: %s" %  args.output[0])


read2cds_solver = None
log.info("read2cds solver: %s" % args.read2cds_solver[0])
if args.read2cds_solver[0] == 'greedy':
    read2cds_solver = GreedySolver()
elif args.read2cds_solver[0] == 'best_score':
    read2cds_solver = BestScoreSolver()

tax_solver = None
log.info("taxonomy solver: %s" % args.tax_solver[0])
if args.tax_solver[0] == 'simple':
    tax_solver = SimpleTaxonomySolver()
elif args.tax_solver[0] == 'simple_join':
    tax_solver = SimpleJoinTaxonomySolver()

log.info("Started.")
solver = Solver(determine_host, read2cds_solver, tax_solver)
solver.generateSolutionXML(args.input[0], args.descr[0], args.output[0])
log.info("Finished.")
