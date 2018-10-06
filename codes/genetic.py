import frame
import random
import unittest
import numpy as NP
import test
from time import time
from astar import aStar, euclideanDist, manhattanDist, chebyshevDist
from bdastar import biDirectionalAStar as BDAStar
from solution import DFS, BFS


class Population:

    def __init__(self, mazeSize, mazeWallRate, populationSize, maxIteration,
                 reproductionRate, mutationRate, hugeMutation = False, weight =
                 [1, 0, 0], solutionFunction = aStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist}):
        self.mazeSize = mazeSize
        self.mazeWallRate = mazeWallRate
        self.populationSize = populationSize
        self.maxIteration = maxIteration
        self.reproductionRate = reproductionRate
        self.mutationRate = mutationRate
        self.hugeMutation = hugeMutation
        self.weight = weight
        self.solutionFunction = globals()[solutionFunction]
        self.solutionConfig = solutionConfig
        if 'distFunction' in solutionConfig:
            self.solutionConfig['distFunction'] = globals()[solutionConfig['distFunction']]
        self.pop = []
        for i in range(self.populationSize):
            if self.mazeWallRate == -1:
                wallRate = random.uniform(0.15, 0.38)
            else:
                wallRate = self.mazeWallRate
            while True:
                m = buildUp(self.mazeSize, wallRate)
                m.score = self.computeFitness(m)
                if m.score == 0:
                    continue
                self.pop += [m]
                break
        self.pop.sort()

    def computeFitness(self, m):
        if m.score != -1:
            return m.score
        blockCount, goalPath, maxFringeSize = self.solutionFunction(m, **self.solutionConfig)
        m.path = goalPath
        if len(goalPath) == 0:
            return 0
        fitness = NP.sum(NP.asarray((blockCount, len(goalPath), maxFringeSize)) * NP.asarray(self.weight))
        return fitness

    def reproduce(self, father, mother):
        #father.visualize()
        #mother.visualize()
        child = buildUp(self.mazeSize, 0.0)
        mid = random.randint(1, self.mazeSize)
        reproductionType = random.randrange(4)
        #reproductionType = 0
        if reproductionType == 2:
            for i in range(self.mazeSize):
                for j in range(self.mazeSize):
                    if j > i:
                        child.wall[i, j] = mother.wall[i, j]
                    else:
                        child.wall[i, j] = father.wall[i, j]
        elif reproductionType == 3:
            for i in range(self.mazeSize):
                for j in range(self.mazeSize):
                    if i + i + j + j > self.mazeSize:
                        child.wall[i, j] = mother.wall[i, j]
                    else:
                        child.wall[i, j] = father.wall[i, j]
        else:
            for i in range(mid):
                if reproductionType == 0:
                    child.wall[:, i] = father.wall[:, i]
                else:
                    child.wall[i, :] = father.wall[i, :]

            for i in range(mid, self.mazeSize):
                if reproductionType == 0:
                    child.wall[:, i] = mother.wall[:, i]
                else:
                    child.wall[i, :] = mother.wall[i, :]

        #child.visualize()
        rollMutation = random.random()
        if rollMutation <= self.mutationRate:
            child = self.mutate(child, self.hugeMutation)
        child.score = self.computeFitness(child)
        return child

    def mutate(self, m, hugeMutation = False):
        mutationTimes = 0
        t = self.mazeSize * self.mazeSize
        if hugeMutation == True:
            mutationTimes = abs(random.randrange(t) - int(t / 2))
        for i in range(mutationTimes):
            x = random.randrange(self.mazeSize)
            y = random.randrange(self.mazeSize)
            m.wall[x][y] ^= 1
        return m

    def nextGeneration(self, pop):
        chosenRate = 0.1
        chosenOnes = int(self.populationSize * chosenRate)
        survive = int(self.populationSize * (self.reproductionRate - chosenRate)) # can use other methods to decide which individual survive
        nextPop = pop[:(self.populationSize - survive)]
        tempPop = pop[-(self.populationSize - survive):]
        random.shuffle(tempPop)
        nextPop += tempPop[:chosenOnes]
        survive += chosenOnes
        probabilityList = []
        sumProbability = 0
        for i in range(self.populationSize):
            sumProbability += pop[i].score
            if i == 0:
                pre = 0
            else:
                pre = probabilityList[i - 1]
            probabilityList += [pre + pop[i].score]
        for i in range(survive):
            flag = True
            while flag:
                father = pop[self.selectParents(sumProbability, probabilityList)]
                mother = pop[self.selectParents(sumProbability, probabilityList)]
                child = self.reproduce(father, mother)
                if child.score != 0:
                    flag = False
            nextPop += [child]
        nextPop.sort()
        return nextPop

    def selectParents(self, sumProbability, probabilityList):
        length = len(probabilityList)
        randomNumber = random.randrange(sumProbability)
        for i in range(length):
            if randomNumber <= probabilityList[i]:
                return i
        return length

    def iterate(self):
        maxFitness = -1
        individualWithMaxFitness = -1
        pop = self.pop
        totalTime = 0
        for iteration in range(self.maxIteration + 1):
            startTime = time()
            pop = self.nextGeneration(pop)
            stopTime = time()
            timePassed = stopTime - startTime
            totalTime += timePassed
            print('iteration: ' + repr(iteration) + ' - ' + repr(pop[0].score) + ' time:' + repr(timePassed))
            if iteration % 10 == 0:
                print('iteration: ' + repr(iteration))
                tempFitness, tempIndividual = printFitness(pop)
                if tempFitness > maxFitness:
                    maxFitness, individualWithMaxFitness = tempFitness, tempIndividual
        #individualWithMaxFitness.visualize()
        self.pop = pop
        print(totalTime)
        return individualWithMaxFitness, pop

    def replaceInitialMazes(self, index, m):
        self.pop[index] = m

    def save(self):
        path = '/common/users/sl1560/temp/'
        name = str(self.solutionFunction.__name__) + '+' + str(self.maxIteration) + '+' + str(self.mutationRate) + '+' + str(self.populationSize) + '.pkl'
        test.saveMaze(self.pop, path, name)

class TestGeneticAlgorithm(unittest.TestCase):

    def testPopulation(self):
        p = Population(25, 0.2, 100, 100, 0.7, 0.1, solutionFunction = aStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist})
        scoreList = []
        for i in p.pop:
            scoreList += [i.score]
        print(scoreList)

    def testReproduce(self):
        p = Population(25, 0.2, 100, 100, 0.7, 0.1, solutionFunction = aStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist})
        t1 = buildUp(25, 0.2)
        t2 = buildUp(25, 0.2)
        child = p.reproduce(t1, t2)
        t1.score = p.computeFitness(t1)
        t2.score = p.computeFitness(t2)
        print(t1.score, t2.score, child.score)

    def testMutate(self):
        p = Population(25, 0.2, 100, 100, 0.7, 0.1)
        t1 = buildUp(25, 0.2)
        #t1.visualize()
        t2 = p.mutate(t1)
        #t2.visualize()

    def testFitness(self):
        p = Population(25, 0.2, 0, 100, 0.7, 0.1, solutionFunction = aStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist})
        t1 = buildUp(25, 0.2)
        print(p.computeFitness(t1))

    def testNextGeneration(self):
        p = Population(25, 0.2, 100, 100, 0.7, 0.1, solutionFunction = aStar, solutionConfig = {'LIFO': True, 'distFunction' : manhattanDist})
        printFitness(p.pop)
        nextGeneration = p.nextGeneration()
        printFitness(nextGeneration)

    def testIteration(self):
        print('Started testing of iteration')
        p = Population(mazeSize = 128, mazeWallRate = -1, populationSize = 500,
                       maxIteration = 120, reproductionRate = 0.7, mutationRate
                       = 0.1, hugeMutation = True, weight = [0, 1, 0],
                       solutionFunction = 'aStar', solutionConfig = {'LIFO':
                                                                     True,
                                                                     'distFunction'
                                                                     :
                                                                     'manhattanDist'})
        finalChild, finalpop = p.iterate()
        print(finalChild, finalpop)
        p.save()
        #finalChild.printMaze()
        #finalChild.visualize()

    def testSave(self):
        p = Population(mazeSize = 32, mazeWallRate = -1, populationSize = 50,
                       maxIteration = 20, reproductionRate = 0.7, mutationRate
                       = 0.05, hugeMutation = True, weight = [0, 1, 0],
                       solutionFunction = 'aStar', solutionConfig = {'LIFO':
                                                                     True,
                                                                     'distFunction'
                                                                     :
                                                                     'manhattanDist'})
        p.save()

def buildUp(mazeSize, mazeWallRate):
    m = frame.maze(rows = mazeSize, cols = mazeSize, p = mazeWallRate)
    m.build(initFunction = None, randomPosition = False, force = False)
    return m

def printFitness(pop):
    maxFitness = -1
    individualWithMaxFitness = -1
    fitnessList = []
    for individual in pop:
        fitnessList += [individual.score]
        if individual.score > maxFitness:
            maxFitness = individual.score
            individualWithMaxFitness = individual
    print(fitnessList)
    return maxFitness, individualWithMaxFitness

if __name__ == '__main__':
    ##unittest.main()
    #mytest = unittest.TestSuite()
    ##mytest.addTest(TestGeneticAlgorithm("testSave"))
    #mytest.addTest(TestGeneticAlgorithm("testIteration"))
    #unittest.TextTestRunner().run(mytest)
    print('Started testing of iteration')
    p = Population(mazeSize = 128, mazeWallRate = -1, populationSize = 500,
                   maxIteration = 120, reproductionRate = 0.7, mutationRate
                   = 0.1, hugeMutation = True, weight = [0, 1, 0],
                   solutionFunction = 'aStar', solutionConfig = {'LIFO':
                                                                 True,
                                                                 'distFunction'
                                                                 :
                                                                 'manhattanDist'})
    finalChild, finalpop = p.iterate()
    print(finalChild, finalpop)
    p.save()
