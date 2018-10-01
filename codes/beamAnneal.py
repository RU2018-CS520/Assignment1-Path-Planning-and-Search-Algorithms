import numpy as np
import random
import math
import timeit

import frame
import localSearch as lS
import test
from solution import BFS, DFS
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar

def beamAnneal(mList, obFn, nebr, teleportLimit = 0, maxIteration = 100, temperature = 10000., coolRate = 0.9, minT = 0.1, annealWeight = 1, annealBias = 4, patience = 100, impatientRate = 0.001):
	#list maze with element frame.maze: init state maze
	#class localSearch.objectiveFunction obFn: evaluate maze score
	#class localSearch.neighbor nebr: generate maze's neighbor maze
	#int maxIteration in [1 : inf]: directly halt searching
	#float temperature in [Tmin, inf]: control probability of simulate annealing, too small may cause early halt
	#float coolRate in [0 : 1]: control temperature decreasing speed. the larger, the slower. 1: disable simulate annealing
	#float minT in [0 : inf]: another way halt searching
	#int or float annealWeight in [0 : inf]: control probablity of simulate annealing. the larger, the smaller.
	#int or float annealBias in [0 : inf]: control probablity of simulate annealing, especially when no effective mutation. the larger, the smaller
	#int patience in [1 : inf]: the last way to halt searching when converged
	#float impatientRate in [0 : inf]: control the number of converged iteration to cause a halt. the larger, the fewer. 0: disable impatient converge halt 
	iterCount = 0
	patienceDecrease = impatientRate
	#prepare for beamSearch
	beamSize = len(mList)
	for i in range(beamSize):
		mList[i].rootNum = i;
	if teleportLimit == 0:
		teleportLimit = int(np.ceil(len(mList) / 4))
	print('start beamAnneal')
	totalStart = timeit.default_timer()
	#start search
	while iterCount < maxIteration and patience > 0 and temperature > minT:
		#get temp score
		tempScore = np.asarray(obFn(mList))
		#print temp result
		print(' iter %i, mean score: %.2f' %(iterCount, np.mean(tempScore)), end = ',')
		startTime = timeit.default_timer()
		#get neighbor score
		tempNext = nebr(mList, validate = True) #CAUTION: validate will dramatically slow down
		nextScore = np.asarray(obFn(tempNext))
		#prepare move to next
		rootCount = np.full(len(mList), teleportLimit, dtype = np.uint8)
		index = list(np.argsort(nextScore))
		index.reverse()
		nextCount = 0
		nextList = []
		noMove = True
		fullBeam = False
		#move to next
		for i in index:
			prevIndex = i // nebr.size
			if nextScore[i] > tempScore[prevIndex] or (coolRate != 1 and random.random() < math.exp((annealWeight * (nextScore[i] - tempScore[prevIndex]) - annealBias) / temperature)):
				candidate = tempNext[i]
				#full teleported agents
				if not candidate.solvable:
					continue
				if rootCount[candidate.rootNum] == 0:
					continue
				rootCount[candidate.rootNum] = rootCount[candidate.rootNum] - 1
				nextList.append(candidate)
				nextCount = nextCount + 1
				noMove = False
			#full beam
			if nextCount == beamSize:
				fullBeam = True
				break
		#add converged agents
		if not fullBeam:
			index = list(np.argsort(tempScore))
			list.reverse
			for i in index:
				candidate = mList[i]
				#full teleported agents
				if rootCount[candidate.rootNum] == 0:
					continue
				rootCount[candidate.rootNum] = rootCount[candidate.rootNum] - 1
				nextList.append(candidate)
				nextCount = nextCount + 1
				if nextCount == beamSize:
					break
		#print time
		endTime = timeit.default_timer()
		print(' for %.2fs' %((endTime - startTime)))
		#cooling
		temperature = temperature * coolRate
		#decrease patience
		iterCount = iterCount + 1
		if noMove:
			patience = patience - iterCount * patienceDecrease
			patienceDecrease = patienceDecrease * 2
		else:
			patienceDecrease = impatientRate
		#prepare new iter
		mList = nextList
	#print result
	totalEnd = timeit.default_timer()
	print('\n********result********')
	if iterCount >= maxIteration:
		print('reached maxIteration')
	if patience <= 0:
		print('no more patience')
	if temperature <= minT:
		print('totally cooled down')
	tempScore = np.asarray(obFn(mList))
	print('final score: %.2f, for %.2fm' %(np.mean(tempScore), ((totalEnd - totalStart) / 60.)))
	return mList

if __name__ == '__main__':
	mList = test.mazeFactory(num = 6, size = 32, p = 0.4)
	sF = BFS
	sC = {'BDBFS' : True, 'quickGoal' : True, 'randomWalk' : True, 'checkFringe' : True}
	obFn = lS.objectiveFunction(w = [0,1,0], solutionFunction = sF, solutionConfig = sC, deRandom = False)
	nebr = lS.neighbor(size = 33, mutationP = 0.02)
	newMaze = beamAnneal(mList, obFn = obFn, nebr = nebr, teleportLimit = 2, maxIteration = 100, temperature = 10000., coolRate = 0.92, minT = 0.1, annealWeight = 16384, annealBias = 8, patience = 100, impatientRate = 0.001)
	path = 'D:/Users/endle/Desktop/520/'
	name = 'newMaze.pkl'
	m = newMaze[0]
	block, mPath, fringe = BFS(m, **sC)
	m.visualize(outerPath = mPath)
#	test.saveMaze(newMaze, path, name) #CAUTION: don't forget to saveMaze