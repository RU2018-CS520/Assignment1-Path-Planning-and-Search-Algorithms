from frame import maze
from solution import DFS, BFS, buildUp
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar
#from idastar import idaStar as IDAStar

import timeit
import pickle as pkl

def vailid(m):
	return BDAStar(m = m, distFunction = manhattanDist, LIFO = True)[1]

def mazeFactory(num = 10, size = 128, p = 0.2, initFunction = None, randomPosition = False, force = False):
	mazeList = []
	i = 0
	while i < num:
		m = buildUp(size, p, initFunction, randomPosition, force)
		if vailid(m):
			mazeList.append(m)
			i = i + 1
	return mazeList

def timer(mazeList, solutionFunction, solutionConfig):
	countList = []
	depthList = []
	startTime = timeit.default_timer()
	print(solutionConfig)
	for m in mazeList:
		count, path, depth = solutionFunction(m, **solutionConfig)
		countList.append(count)
		depthList.append(depth)
	endTime = timeit.default_timer()
	return (countList, depthList, (endTime - startTime))


if __name__ == '__main__':
	mazeList = mazeFactory(num = 10, size = 16, p = 0.2)
	config = {'distFunction' : manhattanDist, 'LIFO' : True}
	countList, depthList, totalTime = timer(mazeList = mazeList, solutionFunction = BDAStar, solutionConfig = config)
	print(countList)
	print(depthList)
	print(totalTime)