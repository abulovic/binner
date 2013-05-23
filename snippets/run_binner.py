import argparse
import sys,os
sys.path.append(os.getcwd())

from solver.Solver import Solver
from solver.taxonomy.SimpleTaxonomySolver       import SimpleTaxonomySolver
from solver.taxonomy.SimpleJoinTaxonomySolver   import SimpleJoinTaxonomySolver
from solver.read2cds.GreedySolver               import GreedySolver
from solver.read2cds.BestScoreSolver            import BestScoreSolver

from utils.logger import Logger


argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='Input alignment file', type=str, nargs=1, dest='input')
argparser.add_argument('-d', '--descr', help='XML description schema', type=str, nargs=1, dest='descr')
argparser.add_argument('-o', '--out', help='Output XML file', type=str, nargs=1, dest='output')
argparser.add_argument('-ts', '--tax_solver', help='Taxonomy solver type', choices=['simple', 'simple_join'], default='simple', nargs=1, dest='tax_solver')
argparser.add_argument('-rs', '--read2cds_solver', help='Read2CDS solver type', choices=['greedy', 'best_score'], default='greedy', nargs=1, dest='read2cds_solver')
argparser.add_argument('-l', '--log', type=str, help='Path to log file', nargs=1, dest='log', default='binner.log')

args = argparser.parse_args()

print args.log

solver = None
if args.tax_solver == 'greedy':
    solver = GreedySolver()
elif args.tax_solver == 'best_score':
    solver = BestScoreSolver()
     
