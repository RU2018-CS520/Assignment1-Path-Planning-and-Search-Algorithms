import timeit
import numpy as np
import math
import random

from solution import BFS, DFS
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar
import test
import localSearch as lS
import beamAnneal as bA
import genetic

def getArg(mazeSize, mazeWallRate, 
			populationSize, gAIteration, reproductionRate, gAMutationRate, hugeMutation, 
			bABeamSize, bANeighborSize, bAMutationRate, validate, teleportLimit, backTeleport, bAIteration, 
			temperature, coolRate, minT, annealWeight, annealBias, patience, impatientRate, tempSave, tempSavePath, 
			weight, solveFun, solveCfg, deRandom, seedMargin, nonPerfectSeedNum):
	#INPUT ARGS:
	#see description
	#RETURN VALS:
	#dict gAArg, oFArg, nbArg, bAArg, alArg: input args
	
	#genetic
	gASvFun = solveFun.__name__
	gASvCfg = solveCfg
	if 'distFunction' in solveCfg:
		gASvCfg['distFunction'] = solveCfg['distFunction'].__name__
	gAArg = {'mazeSize': mazeSize, 'mazeWallRate' : mazeWallRate, 'populationSize' : populationSize, 
			'maxIteration' : gAIteration, 'reproductionRate' : reproductionRate, 'mutationRate' : gAMutationRate, 'hugeMutation' : hugeMutation,
			'weight' : weight, 'solutionFunction' : gASvFun, 'solutionConfig' : gASvCfg}
	#objectiveFunction
	oFArg = {'w' : weight, 'solutionFunction' : solveFun, 'solutionConfig' : solveCfg, 'deRandom' : deRandom}
	#neighbor
	nbArg = {'size' : bANeighborSize, 'mutationP' : bAMutationRate}
	#beamAnneal
	bAArg = {'validate' : validate, 'teleportLimit' : teleportLimit, 'backTeleport' : backTeleport, 
			'maxIteration' : bAIteration, 'temperature' : temperature, 'coolRate' : coolRate, 'minT' : minT, 'annealWeight' : annealWeight, 'annealBias' : annealBias, 
			'patience' : patience, 'impatientRate' : impatientRate, 'tempSave' : tempSave, 'savePath' : tempSavePath, 'suffix' : str(weight)}
	alArg = {'logPath' : tempSavePath, 'beamSeedNum': bABeamSize, 'seedMargin' : seedMargin, 'nonPerfectSeedNum' : nonPerfectSeedNum, 'suffix' : str(weight)}
	return (gAArg, oFArg, nbArg, bAArg, alArg)

def alchemy(gAArg, bAArg, obFn, nebr, logPath, beamSeedNum, seedMargin, nonPerfectSeedNum, suffix):
	#INPUT ARGS:
	#dict gAArg, bAArg:
	#class obFn nebr:
	#str logPath: used for save log mazes
	#int beamSeedNum in [1 : genetic.populationSize]: size of beam search
	#int nonPerfectSeedNum [0 : beamSeedNum]: the number of seed could be not enough good

	#RETURN VAL:
	#list finalMaze with element frame.maze: finetuned mazes

	#genetic
	gAPopulation = genetic.Population(**gAArg)
	print('start genetic')
	gAStartTime = timeit.default_timer()
	finalChild, finalPopulation = gAPopulation.iterate()
	gAEndTime = timeit.default_timer()
	seedScore = np.asarray(obFn(finalPopulation))
	print('\n********genetic result********')
	print('final score: %.2f, for %.2fm' %(np.mean(seedScore), ((gAEndTime - gAStartTime) / 60.)))
	test.saveMaze(finalPopulation, logPath, 'geneticFinalMazeList' + suffix + '.pkl')
	#prepare for beamAnneal
	index = list(np.argsort(seedScore))
	maxSeedScore = seedScore[index[-1]]
	#increase diversity
	nonPerfectSeedCount = 0
	seedList = []
	for i in range(len(index)):
		if i - nonPerfectSeedCount < len(index) - beamSeedNum:
			if nonPerfectSeedNum == 0 or seedScore[index[i]] < seedMargin * maxSeedScore: #too low score
				continue
			probablity = math.exp((maxSeedScore / seedScore[index[i]]) * -2)
			if random.random() < probablity:
				seedList.append(finalPopulation[index[i]])
				nonPerfectSeedCount = nonPerfectSeedCount + 1
				if nonPerfectSeedCount == nonPerfectSeedNum:
					seedList.extend(list(np.asarray(finalPopulation)[index[-(beamSeedNum-nonPerfectSeedNum):]]))
					break
		else:
			seedList.extend(list(np.asarray(finalPopulation)[index[i:]]))
			break
	#beamAnneal
	bAStartTime = timeit.default_timer()
	finalMaze = bA.beamAnneal(seedList, obFn = obFn, nebr = nebr, **bAArg)
	bAEndTime = timeit.default_timer()
	#printout
	finalScore = np.asarray(obFn(finalMaze))
	index = list(np.argsort(finalScore))
	index.reverse()
	finalMaze = list(np.asarray(finalMaze)[index])
	gAIndex = 0
	for i in range(len(index)):
		if finalMaze[i].score < finalPopulation[gAIndex].score:
			finalMaze[i] = finalPopulation[gAIndex]
			gAIndex = gAIndex + 1
	print('\n\n************final result************')
	print('final score: %.2f, %.2f, etc., for %.2fm in total' %(finalMaze[0].score, finalMaze[1].score, ((bAEndTime - gAStartTime) / 60.)))
	return finalMaze

if __name__ == '__main__':
	#maze
	mazeSize = 16 #test 16 first
	mazeWallRate = -1
	#genetic
	populationSize = 16 #test 16 first
	gAIteration = 16 #test 16 first
	reproductionRate = 0.7
	gAMutationRate = 0.1
	hugeMutation = True
	#beam simulated annealing
	bABeamSize = 5
	bANeighborSize = 20
	bAMutationRate = 0.001
	validate = True
	teleportLimit = 2
	backTeleport = True
	bAIteration = 16 #test 16 first
	temperature = 100.
	coolRate = 0.945
	minT = 0.001
	annealWeight = 1024
	annealBias = 8
	patience = 100
	impatientRate = 0.001
	tempSave = 10
	tempSavePath = 'D:/Users/endle/Desktop/520/log/'
	#objectiveFunction
	weight = [0, 1, 0]
	solveFun = aStar
	solveCfg = {'distFunction' : manhattanDist, 'LIFO' : True}
	deRandom = False
	#others
	seedMargin = 0.95
	nonPerfectSeedNum = 3
	resultPath = 'D:/Users/endle/Desktop/520/'
	resultName = 'finalMazeList.pkl'
	#get args
	gAArg, oFArg, nbArg, bAArg, alArg = getArg(mazeSize = mazeSize, mazeWallRate = mazeWallRate, 
										populationSize = populationSize, gAIteration = gAIteration, reproductionRate = reproductionRate, gAMutationRate = gAMutationRate, hugeMutation = hugeMutation, 
										bABeamSize = bABeamSize, bANeighborSize = bANeighborSize, bAMutationRate = bAMutationRate, validate = validate, teleportLimit = teleportLimit, backTeleport = backTeleport, bAIteration = bAIteration, 
										temperature = temperature, coolRate = coolRate, minT = minT, annealWeight = annealWeight, annealBias = annealBias, patience = patience, impatientRate = impatientRate, tempSave = tempSave, tempSavePath = tempSavePath, 
										weight = weight, solveFun = solveFun, solveCfg = solveCfg, deRandom = deRandom, seedMargin = seedMargin, nonPerfectSeedNum = nonPerfectSeedNum)
	obFn = lS.objectiveFunction(**oFArg)
	nebr = lS.neighbor(**nbArg)
	#god knows...
	finalMaze = alchemy(gAArg = gAArg, bAArg = bAArg, obFn = obFn, nebr = nebr, **alArg)
	#CAUTION SAVE IT!
	test.saveMaze(finalMaze, resultPath, str(weight) + resultName)
