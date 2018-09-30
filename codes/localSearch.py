import numpy as np

import frame
from bdastar import biDirectionalAStar as BDAStar, euclideanDist, manhattanDist, chebyshevDist
from test import mazeFactory

class objectiveFunction(object):
	"""docstring for objectiveFunction"""
	def __init__(self, w = [1, 0, 0], solutionFunction = BDAStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist}, deRandom = False):
		#list w with len(w) = 3: weight of blockCount, pathLength, fringeSize
		#function solutionFunction: algorithms to be tested
		#dict solutionConfig: configuration of solutionFunction. see description
		#bool or int deRandom: True: run another int(deRandom) times to get a min score; False: the algorithm is not random
		self.w = w
		self.solutionFunction = solutionFunction
		self.solutionConfig = solutionConfig
		self.deRandom = deRandom

	def __call__(self, maze):
		#class frame.maze or list maze with element frame.maze: maze to be evaluate
		def evaluate(m, w, solutionFunction, solutionConfig, deRandom):
			if isinstance(m, frame.maze):
				block, path, fringe = solutionFunction(m, **solutionConfig)
				if path:
					result = np.sum(np.asarray((block, len(path), fringe)) * np.asarray(w))
					while deRandom:
						block, path, fringe = solutionFunction(m, **solutionConfig)
						result = np.min((result, np.sum(np.asarray((block, len(path), fringe)) * np.asarray(w))))
						deRandom = int(deRandom) - 1
					return result
				else:
					return 0
			else:
				print('E: localSearch.objectiveFunction.__call__(), not a maze input')
				exit()
		
		if isinstance(maze, list) or isinstance(maze, tuple):
			resultList = []
			for m in maze:
				resultList.append(evaluate(m, self.w, self.solutionFunction, self.solutionConfig, self.deRandom))
			return resultList
		else:
			return evaluate(maze, self.w, self.solutionFunction, self.solutionConfig, self.deRandom)

def beamSearch(mList, teleportLimit = 0, maxIteration = 100, temperature, ):
	pass

if __name__ == '__main__':
	a = frame.maze()
	a.build()
	b = frame.maze()
	b.build()
	sf = BDAStar
	sc = {'LIFO': True, 'distFunction' : manhattanDist}
	of = objectiveFunction([1,1,1], sf, sc, deRandom = 2)
	print(of([a,b]))
	print(BDAStar(a, **sc))