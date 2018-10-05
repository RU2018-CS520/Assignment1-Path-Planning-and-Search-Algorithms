import sys
import ast
import json
import test
from genetic import Population

if __name__ == '__main__':
    argu1 = ast.literal_eval(sys.argv[1])
    #argu1 = sys.argv[1]
    #argu2 = ast.literal_eval(sys.argv[2])
    #print(argu1)
    p = Population(**argu1)
    finalchild, finalPopulation = p.iterate()
    p.save()
    #p = Population(**sys.argv[1])
    #arguments = sys.argv[1].replace("'", "\"")
    #p = Population(json.loads(arguments))
