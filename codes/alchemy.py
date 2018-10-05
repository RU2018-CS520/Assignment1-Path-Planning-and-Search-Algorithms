import timeit

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
			weight, solveFun, solveCfg, deRandom):
	#INPUT ARGS:
	#see description
	#RETURN VALS:
	#dict gAArg, oFArg, nbArg, bAArg: input args
	
	#genetic
	gASvFun = solveFun.__name__
	gASvCfg = solveCfg
	if 'distFunction' in solutionConfig:
		gASvCfg['distFunction'] = solveCfg['distFunction'].__name__
	gAArg = {'mazeSize': mazeSize, 'mazeWallRate' : mazeWallRate, 'populationSize' : populationSize, 
			'maxIteration' : gAIteration, 'reproductionRate' : reproductionRate, 'mutationRate' : gAMutationRate, 'hugeMutation' : hugeMutation
			'weight' : weight, 'solutionFunction' : gASvFun, 'solutionConfig' : gASvCfg}
	#objectiveFunction
	oFArg = {'w' : weight, 'solutionFunction' : solveFun, 'solutionConfig' : solveCfg, 'deRandom' : deRandom}
	#neighbor
	nbArg = {'size' : bANeighborSize, 'mutationP' : bAMutationRate}
	#beamAnneal
	bAArg = {'validate' : validate, 'teleportLimit' : teleportLimit, 'backTeleport' : backTeleport, 
			'maxIteration' : bAIteration, 'temperature' : temperature, 'coolRate' : coolRate, 'minT' : minT, 'annealWeight' = annealWeight, 'annealBias' = annealBias, 
			'patience' : patience, 'impatientRate' : impatientRate, 'tempSave' : tempSave, 'savePath' : tempSavePath}
	return (gAArg, oFArg, nbArg, bAArg)

if __name__ == '__main__':
	#maze
	mazeSize = 128
	mazeWallRate = -1
	#genetic
	populationSize = 750
	gAIteration = 130
	reproductionRate = 0.7
	gAMutationRate = 0.05
	hugeMutation = True
	#beam simulated annealing
	bABeamSize = 5
	bANeighborSize = 20
	bAMutationRate = 0.001
	validate = True
	teleportLimit = 2
	backTeleport = True
	bAIteration = 200
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
	solveCfg = {'distFunction' : manhattanDist, 'LIFO' = True}
	deRandom = False
	#others


	gaArg, oFArg, nbArg, bAArg = getArg(mazeSize = mazeSize, mazeWallRate = mazeWallRate, 
										populationSize = populationSize, gAIteration = gAIteration, reproductionRate = reproductionRate, gAMutationRate = gAMutationRate, hugeMutation = hugeMutation, 
										bABeamSize = bABeamSize, bANeighborSize = bANeighborSize, bAMutationRate = bAMutationRate, validate = validate, teleportLimit = teleportLimit, backTeleport = backTeleport, bAIteration = bAIteration, 
										temperature = temperature, coolRate = coolRate, minT = minT, annealWeight = annealWeight, annealBias = annealBias, patience = patience, impatientRate = impatientRate, tempSave = tempSave, tempSavePath = tempSavePath, 
										weight = weight, solveFun = solveFun, solveCfg = solveCfg, deRandom = deRandom)
	obFn = lS.objectiveFunction(oFArg)
	nebr = ls.neighbor(nbArg)
	