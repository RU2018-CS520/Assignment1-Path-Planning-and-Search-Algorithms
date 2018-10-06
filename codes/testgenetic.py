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
    path = '/common/users/sl1560/temp/'
    name = 'aStar+120+0.1+500.pkl'
    p = Population(**argu1)
    pp = test.loadMaze(path, name)
    for i in range(1):
        p.replaceInitialMazes(i, pp[i])
        print('changed', pp[i].score)
    finalchild, finalPopulation = p.iterate()
    p.save()
    #finalchild.visualize()
    #p = Population(**sys.argv[1])
    #arguments = sys.argv[1].replace("'", "\"")
    #p = Population(json.loads(arguments))
