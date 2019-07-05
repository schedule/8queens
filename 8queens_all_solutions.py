# (c) imreszakal.com

from ortools.sat.python import cp_model
import time

import numpy as np
from matplotlib import pyplot as plt

table_size = 8 # Select table size

print('.......................................................................')

print()
print('Table size:', table_size)

start = time.time()

results = []
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        counter = 0
        result = ''
        for v in self.__variables:
            if self.Value(v) == 1:
                counter += 1
                result += str(v) + ' '
                # print(v, end=' ')
        if counter == table_size:
            results.append(result)
        # print()

    def solution_count(self):
        return self.__solution_count


def SearchForAllSolutionsSampleSat():
    """Showcases calling the solver to search for all solutions."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    queen = {}
    horizontal = [i for i in range(table_size)]
    vertical = [j for j in range(table_size)]
    for i in horizontal:
        for j in vertical:
            n = '{}.{}'.format(i,j)
            queen[(i,j)] = model.NewBoolVar(n)

    # Create the constraints.
    cover = {}
    for i in horizontal:
        for j in vertical:
            d1 = [[i+k,j+k] for k in range(-table_size+1, table_size) if
                    (i+k>=0 and i+k<=table_size-1 and j+k>=0 and j+k<=table_size-1)]
            d1.remove([i,j])
            d2 = [[i+k,j-k] for k in range(-table_size+1, 8) if
                    (i+k>=0 and i+k<=table_size-1 and j-k>=0 and j-k<=table_size-1)]
            d2.remove([i,j])
            d = d1 + d2

            h = [[i,k] for k in vertical]
            v = [[l,j] for l in horizontal]
            hv = h + v
            hv.remove([i,j])
            hv.remove([i,j])

            cover[(i,j)] = d + hv # [i,j] is not in it

    for i in horizontal:
        for j in vertical:
            for k in cover[(i,j)]:
                model.Add(queen[(i,j)] + queen[(k[0],k[1])] <= 1)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([queen[(i,j)]
            for i in horizontal for j in vertical])
    status = solver.SearchForAllSolutions(model, solution_printer)

    # print()
    # print('Status = %s' % solver.StatusName(status))
    # print('Number of solutions found: %i' % solution_printer.solution_count())


SearchForAllSolutionsSampleSat()

end = time.time()

print()
print('Full size solutions:', len(results))
for result in results:
    print(result)

print()
print('Time:')
print('{:.8f} seconds'.format(end - start))
print()
