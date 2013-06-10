import logging
import logging.config
import argparse
import sys,os
sys.path.append(os.getcwd())

from statistics.ComparisonData import ComparisonData
from statistics.solutiondata import loadOrganismData


def parse_input_parameters():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Compares two xml output files '
        'file')
    argparser.add_argument('solution_xml', help='Correct solution', 
                           type=str)
    argparser.add_argument('solver_xml', help="Solver's solution", 
                           type=str)

    args = argparser.parse_args()
    
    error = False
    if not os.path.exists(os.path.expanduser(args.solution_xml)):
        print "Solution xml file %s doesn't exist" % args.solution_xml
        error = True
    if not os.path.exists(os.path.expanduser(args.solver_xml)):
        print "Solver xml file %s doesn't exist" % args.solver_xml
        error = True
    if error:
        exit(-1)

    return args

if __name__ == '__main__':
    args = parse_input_parameters()

    solution_data = loadOrganismData(args.solution_xml)
    solver_data = loadOrganismData(args.solver_xml)

    cd = ComparisonData.solution_data_vs_solution_data(solution_data, solver_data)

    print cd.shortStr()
