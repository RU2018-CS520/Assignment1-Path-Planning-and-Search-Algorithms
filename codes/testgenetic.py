import sys
import ast
import json
from genetic import Population
from astar import aStar as aS, euclideanDist, manhattanDist, chebyshevDist

if __name__ == '__main__':
    argu1 = ast.literal_eval(sys.argv[1])
    #argu1 = sys.argv[1]
    #argu2 = ast.literal_eval(sys.argv[2])
    #print(argu1)
    p = Population(**argu1)
    finalchild = p.iterate()
    print(finalchild)
    #p = Population(**sys.argv[1])
    #arguments = sys.argv[1].replace("'", "\"")
    #p = Population(json.loads(arguments))
