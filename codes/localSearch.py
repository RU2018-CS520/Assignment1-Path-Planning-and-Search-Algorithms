import numpy as np

import frame
from bdastar import biDirectionalAStar as BDAStar, euclideanDist, manhattanDist, chebyshevDist
from test import mazeFactory as mFty

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
		return

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

class neighbor(object):
	"""docstring for neighbor"""
	def __init__(self, size = 4, mutationP = 0.001, mutationFunction = None, mutationConfig = None):
		self.size = size
		self.mutationP = mutationP
		self.mutationFunction = mutationFunction
		self.mutationConfig = mutationConfig

	def __call__(self, maze, validate = False):
		#class frame.maze or list maze with element frame.maze: maze to be evaluate
		#bool validate: True: keep neighbor solvable, CAUTION: may cause endless loop; False: neighbor can be unsolvable

		def mutation(m, mutationP, mutationFunction, mutationConfig, validate):

			def trivalMutation(m, mutationP, validate):
				mutationMatrix = np.random.rand(m.shape) < mutationP
				return m.wall ^ mutationMatrix

			if isinstance(m, frame.maze):
				newMazeList = []
				count = 0
				while count < size:
					if mutationFunction is None:
						wall = trivalMutation(m, mutationP)
					else:
						#TODO: other mutationFunction
						pass
					newMaze = frame.maze(m.rows, m.cols, m.p, m.rootNumber)
					newMaze.build(initFunction = frame.maze.build.setWall, initConfig = {'wall': wall})
					if validate and not mFty.valid(newMaze):
						continue
					newMazeList.append(newMaze)
					count = count + 1
				return newMazeList
			else:
				print('E: localSearch.neighbor.__call__(), not a maze input')
				exit()

		if isinstance(maze, list) or isinstance(maze, tuple):
			neighborList = []
			for m in maze:
				resultList.extend(mutation(m, self.mutationP, self.mutationFunction, self.mutationConfig, self.validate))
			return neighborList
		else:
			return mutation(m, self.mutationP, self.mutationFunction, self.mutationConfig, self.validate))
		

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