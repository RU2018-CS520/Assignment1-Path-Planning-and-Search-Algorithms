from frame import maze
from solution import DFS, BFS, buildUp
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar

import timeit
import pickle as pkl

def valid(m):
	return BDAStar(m = m, distFunction = manhattanDist, LIFO = True)[1]

def mazeFactory(num = 10, size = 128, p = 0.2, initFunction = None, randomPosition = False):
	#INPUT ARGS:
	#int num in [1 : inf]: the number of mazes in the test list
	#int size in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a block becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	#RETURN VALS:
	#list mazeList with element class maze: test set of mazes
	
	mazeList = []
	i = 0
	while i < num:
		m = buildUp(size, p, initFunction, randomPosition)
		if valid(m): #keep test set solvable
			mazeList.append(m)
			i = i + 1
	return mazeList

def timer(mazeList, solutionFunction, solutionConfig):
	#INPUT ARGS:
	#list mazeList with element class maze: test set of mazes
	#function solutionFunction: algorithms to be tested
	#dict solutionConfig: configuration of solutionFunction. see description
	#RETURN VALS:
	#list countList with element int blockCount: the number of blocks have opend in each maze
	#list pathList with element int pathLength: the length of path returned in each maze
	#list fringeList with element int maxFringeSize: the max size of fringe in each maze
	#float totalTime: the total time spend for solving all the mazes
	countList = []
	pathList = []
	fringeList = []
	startTime = timeit.default_timer()
	for m in mazeList:
		count, path, fringe = solutionFunction(m, **solutionConfig)
		countList.append(count)
		pathList.append(len(path))
		fringeList.append(fringe)
	endTime = timeit.default_timer()
	return (countList, pathList, fringeList, (endTime - startTime))

def saveMaze(mazeList, path, name):
	#list mazeList with element class maze: test set of mazes. acturally, anything is ok
	#str path: saved file path. REMEMBER: end with a slash
	#str name: saved file name
	saveFile = open(path+name, 'wb')
	pkl.dump(mazeList, saveFile)
	saveFile.close()
	return

def loadMaze(path, name):
	#INPUT ARGS:
	#str path: saved file path. REMEMBER: end with a slash
	#str name: saved file name
	#RETURN VAL:
	#list mazeList with element class maze: test set of mazes. acturally, can be anything
	loadFile = open(path+name, 'rb')
	mazeList = pkl.load(loadFile)
	loadFile.close()
	return mazeList

if __name__ == '__main__':
	mazeList = mazeFactory(num = 10, size = 30, p = 0.3)
	path = 'D:/Users/endle/Desktop/520/'
	name = 'mazeList.pkl'
#	saveMaze(mazeList, path, name)
#	mazeList = loadMaze(path, name)
	config = {}
	countList, pathList, depthList, totalTime = timer(mazeList = mazeList, solutionFunction = BFS, solutionConfig = config)
	print(countList)
	print(pathList)
	print(depthList)
	print(totalTime)