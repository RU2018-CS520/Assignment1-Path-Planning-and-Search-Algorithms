from frame import maze
from solution import DFS, BFS, buildUp
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar

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
	pathList = []
	fringeList = []
	startTime = timeit.default_timer()
	print(solutionConfig)
	for m in mazeList:
		count, path, fringe = solutionFunction(m, **solutionConfig)
		countList.append(count)
		pathList.append(len(path))
		fringeList.append(fringe)
	endTime = timeit.default_timer()
	return (countList, pathList, fringeList, (endTime - startTime))

def saveMaze(mazeList, path, name):
	saveFile = open(path+name, 'wb')
	pkl.dump(mazeList, saveFile)
	saveFile.close()
	return

def loadMaze(path, name):
	loadFile = open(path+name, 'rb')
	mazeList = pkl.load(loadFile)
	loadFile.close()
	return mazeList

if __name__ == '__main__':
	mazeList = mazeFactory(num = 10, size = 16, p = 0.2)
	path = 'D:/Users/endle/Desktop/520/'
	name = 'mazeList.pkl'
	saveMaze(mazeList, path, name)
	mazeList = loadMaze(path, name)
	config = {'distFunction' : manhattanDist, 'LIFO' : True}
	countList, pathList, depthList, totalTime = timer(mazeList = mazeList, solutionFunction = BDAStar, solutionConfig = config)
	print(countList)
	print(pathList)
	print(depthList)
	print(totalTime)