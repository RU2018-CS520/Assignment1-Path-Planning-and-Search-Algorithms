# file description

## frame
a basic frame for MazeRunner, with class maze.

### class maze()
**member vars:**
```
int rows in [2 : inf]:
int cols in [2 : inf]:
float p in [0 : 1]:
np.array wall with ndim = 2 dtype = np.bool: True: this block is a wall; False: accessible empty block
list path with element (row, col): a path from S to G. None or [] if not exist
np.array closed with ndim = 2 dtype = np.bool: True: block is in closed set; False: cast off closed set
(row, col) start: start point, default (0, 0)
(row, col) goal: destination, default (rows-1, cols-1)
bool isBuilt: True: has built up walls, do NOT build it again; False: empty maze, call function build() before solove it
int rootNum in [0 : inf]: record of the root, used in beam search
bool solvable: True: there must be a path. False: no path or untested(check maze.score)
int or float score in [0 : inf]: objectiveFunction(maze)
class maze teleported: previous root maze, used in beamAnneal. last for only 1 generation
```

**member funcs:**
```
build(): build up walls, define maze.start and maze.goal
visualize(): plot maze map with path if exist, return a PIL.Image.Image img
```

**usage:**

build and print 10 same-size mazes
```
import frame
m = frame.maze(rows = 5, cols = 5, p = 0.2)
for i in range(10):
	m.build(force = True)
	m.visualize()
```
process path
```
import frame
import solution
m = frame.maze()
m.build()
blockCount, path, depth = solution.DFS(m, quickGoal = True, randomWalk = True, checkFringe = True) #see description.solution.DFS
m.path = path
if m.path:
	foobar(m.path)
```
save map
```
import frame
import solution
m = frame.maze()
m.build()
count, path, depth = solution.DFS(m)
img = m.visualize(size = 10, grid = 1, outerPath = path)
iPath = 'D:/Users/endle/Desktop/520/'
iName = 'maze.png'
img.save(iPath+iName, 'PNG')
```
build with setWall
```
import frame
m = frame.maze()
wall = foobar() #see neighbor
m.build(initFunction = frame.setWall, initConifg = {'wall' : wall})
```

## solution
a number of algorithms to solve the maze, including Depth-First Search, Breadth-First Search, and their variants.

### DFS()
**input args:**
```
class maze m:
bool IDDFS: 
	True: IDDFS. promise optimal if expand(updatable), but if checkFringe, very slow
	False: DFS. much absolutely faster
	CAUTION: if keepSearch: force keepSearch = False
bool keepSearch incompatible with quickGoal, distinctFringe: 
	True: not return until empty fringe. promise optimal if expand(updatable)
		CAUTION: incredibly slow, checkFringe may accelerate dramatically
		CAUTION: Force expand(updatable = True)
	False: return as soon as goal. usually faster
	CAUTION: if IDDFS: force keepSearch = False
	CAUTION: if quickGoal: force keepSearch = checkFringe, quickGoal = False
bool quickGoal incompatible with keepSearch:
	True: immediately return when push goal into fringe. in this case, DFS, effective and without any cost
	False: return when pop goal out from fringe
	CAUTION: if keepSearch: force keepSearch = checkFringe, quickGoal = False
bool randomWalk: 
	True: partially randomly pick a neighbor as next block. priority: R and D > L and U, might work well;
	False: priority: strictly R > D > L > U, seems effective in this diagonal maze
bool randomWalkPlus: 
	True: totally random, no priority. may be effictive when maze.build(randomPosition)
		CAUTION: force randomWalk = True
	False: depend on randomWalk
bool distinctFringe incompatible with checkFringe, keepSearch: 
	True: keep fringe distinct, and closed block will be always closed
	False: just keep no back turning, but can visit a block twice
bool checkFringe incompatible with distinctFringe:
	True: besides closed set, keep fringe distinct. to some extent, return a shorter path, but not definitely shortest; 
		CAUTION: force expand(updatable = Ture)
	False: just keep no back turning. a little bit faster if not IDDFS
```
**return vals:**
```
int blockCount in [1 : inf]: The number of blocks has been opened. A reference of how hard the maze is.
list goalPath with element (row, col): a path from S to G. [] if not exist. REMEMBER: maze.path = goalPath
int maxFringe in [1 : inf]: The max size of this algorithm's fringe. Another reference of how hard the maze is.
```

**==issue regarding distinctFringe and checkFringe==**
Theoretically, both of them should search the fringe to check if the block to be pushed has already been in the fringe. However, it takes too much time to do so. Therefore, we push those nodes first, and check them whether have been added in closed set when popping out. In this case, it can be done in a constant time.

**usage:**

DFS
```
import solution
m = solution.buildUp() #see solution.others
m.visualize() #see description.frame.maze
count, path, depth = solution.DFS(m) #just ordinary DFS
```
IDDFS
```
import solution
m = solution.buildUp()
m.visualize()
count, path, depth = solution.DFS(m, IDDFS = True, checkFringe = False) #slow
m.build(force = True) #see description.frame.maze
count, path, depth = solution.DFS(m, IDDFS = True, checkFringe = True) #very slow, but optimal
```
DFS (keep searching)
```
import solution
m = solution.buildUp()
count, path, depth = solution.DFS(m, keepSearching = True, checkFringe = False) #extremely slow, but optimal
m.build(force = True)
count, path, depth = solution.DFS(m, keepSearching = True, checkFringe = True) #a little bit faster, still optimal
```
DFS (quick goal)
```
import solution
m = solution.buildUp()
count, path, depth = solution.DFS(quickGoal = True) #faster
```
DFS (random walk)
```
import solution
m = solution.buildUp()
count, path, depth = solution.DFS(randomWalk = True) #sometimes effective
m.build(randomPosition = True, force = True)
count, path, depth = solution.DFS(randomWalkPlus = True) #work well with buildUp(randomPosition = True)
```
DFS (check fringe)
```
import solution
m = solution.buildUp()
count, path, depth = solution.DFS(checkFringe = True) #sometimes useful, but sometime terrible(especially when walls blocked Goal)
```
DFS (today's special)
```
import solution
m = solution.buildUp()
count, path, depth = solution.DFS(quickGoal = True, randomWalk = True) #because it is coooooooooooool
```

### BFS()
**input args**
```
class maze m:
bool BDBFS:
	True: BDBFS. much faster is there is no path.
	False: BFS. in this case, maze runner, no advantage.
bool quickGoal: 
	True: immediately return when push goal into fringe, in this case, BFS, effective and without any cost; 
	False: return when pop goal out from fringe
bool randomWalk: 
	True: partially randomly pick a neighbor as next block. priority: R and D > L and U, might work well;
	False: priority: strictly R > D > L > U, seems effective in this diagonal maze
bool randomWalkPlus: 
	True: totally random, no priority. may be effective when maze.build(randomPosition)
		CAUTION: force randomWalk = True
	False: depend on randomWalk
bool checkFringe:
	True: besides closed set, keep fringe distinct. faster
	False: just keep no back turning.
int depthLimit in [1 : inf]: 
	used to limit depth explores, 0 if n/a
```

**return vals:**
```
int blockCount in [1 : inf]: The number of blocks has been opened. A reference of how hard the maze is.
list goalPath with element (row, col): a path from S to G. [] if not exist. REMEMBER: maze.path = goalPath
int maxFringe in [1 : inf]: The max size of this algorithm's fringe. Another reference of how hard the maze is.
```

**usage:**

BFS
```
import solution
m = solution.buildUp() #see solution.others
m.visualize() #see description.frame.maze
count, path, depth = solution.BFS(m) #just ordinary BFS
```
BDBFS
```
import solution
m = solution.buildUp()
count, path, depth = solution.BFS(m, BDBFS = True) #Better Defination of BFS, LOL
```
BFS (quick goal)
```
import solution
m = solution.buildUp()
count, path, depth = solution.BFS(m, quickGoal = True) #faster
```
BFS (random walk)
```
import solution
m = solution.buildUp()
count, path, depth = solution.BFS(m, randomWalk = True) #sometimes effective
m.build(randomPosition = True, force = True)
count, path, depth = solution.BFS(m, randomWalkPlus = True) #work well with buildUp(randomPosition = True)
```
BFS (check fringe)
```
import solution
m = solution.buildUp()
count, path, depth = solution.BFS(m, checkFringe = True) #also faster
```
BFS (today's special)
```
import solution
m = solution.buildUp()
count, path, depth = solution.BFS(m, BDBFS = True, quickGoal = True, randomWalk = True, checkFringe = True) #because it is coooooooooooool
```

## astar.py  
### aStar(m, distFunction, LIFO)  
**input args**  
```
class maze m: Maze to be solved.  
function distFunction: The function of distance calculation astar is going to use. The default distFunction is manhattanDist. Other choices include euclideanDist and chebyshevDist.  
bool LIFO: Enable Last-In-First-Out priority queue if LIFO is set to True.  
	CAUTION: default is True
```
**return vals**
```
int blockCount in [1 : inf]: The number of blocks has been opened. A reference of how hard the maze is.
list goalPath with element (row, col): a path from S to G. [] if not exist. REMEMBER: maze.path = goalPath
int maxFringe in [1 : inf]: The max size of this algorithm's fringe. Another reference of how hard the maze is.
```
**usage:**  
In the input arguments, distFunction could be **euclideanDist**, **manhattanDist** and **chebyshevDist**. LIFO could be **True** or **False**.  
The following code is a sample of astar using euclideanDist and not using LIFO.
```
import astar

m = astar.buildUp(size = 128, p = 0.35)
blockCount, goalPath, maxFringe = astar.astar(m, distFunction = euclideanDist, LIFO = False)
```

## bdastar
a variant of A\*, Bi-Directional A\*, seems **not optimal**

### biDirectionalAStar()
see *description.astar.aStar()*

## test
a brunch of functions used to test algorithms

### mazeFactory()
**input args:**
```
int num in [1 : inf]: the number of mazes in the test list
int size in [2 : inf]: maze width and height
float p in [0 : 1]: probablity of a block becomes a wall
	CAUTION: a too big p could cause endless loop
function initFunction: init walls, None default trivalInit()
bool randomPosition: 
	True: randomlize start and goal position
	False: start at upper left and goal at lower right
```
**return val:**
```
list mazeList with element class maze: test set of mazes
```

**usage:**

create 10 mazes
```
import test
mazeList = test.mazeFactory(num = 10, size = 16, p = 0.2)
```

### timer()
**input args:**
```
list mazeList with element class maze: test set of mazes
function solutionFunction: algorithms to be tested
dict solutionConfig: configuration of solutionFunction. see each algorithm's input args and usage
```
**return vals:**
```
list countList with element int blockCount: the number of blocks has opend in each maze
list pathList with element int pathLength: the length of path returned in each maze
list fringeList with element int maxFringeSize: the max size of fringe in each maze
float totalTime: the total time spend for solving all the mazes
```

**usage**

test BDA* with manhattanDist
```
from bdastar import aStar, manhattanDist
import test
mazeList = test.mazeFactory(num = 10, size = 16, p = 0.2)
config = {'distFunction' : manhattanDist, 'LIFO' : True}
countList, pathList, depthList, totalTime = test.timer(mazeList = mazeList, solutionFunction = BDAStar, solutionConfig = config)

```

### saveMaze() & loadMaze
**input args:**
```
str path: saved file path. REMEMBER: end with a slash
str name: saved file name
```
**input arg** ***OR*** **return val:**
```
list mazeList with element class maze: test set of mazes. actually, can be anything
```

**usage:**

save something
```
import test
mazeList = mazeFactory()
path = 'D:/Users/endle/Desktop/520/'
name = 'mazeList.pkl'
test.saveMaze(mazeList, path, name)
```
load something
```
import test
path = 'D:/Users/endle/Desktop/520/'
name = 'mazeList.pkl'
mazeList = loadMaze(path, name)
```

## localSearch
some useful tools for local search

### class objectiveFunction()
**member vars:**
```
list w with element int or float len(w) = 3: weight
function solutionFunction:
dict solutionConfig: see description.solution, description.astar and description.bdastar
bool or int deRandom: cast more test to get a min score
```

**usage:**
get mazes' socre
```
import test
import localSearch
from bdastar import biDirectionalAStar as BDAStar, manhattanDist
mList = test.mazeFactory()
sf = BDAStar
sc = {'LIFO': True, 'distFunction' : manhattanDist}
obFn = localSearch.objectiveFunction([1,1,1], sf, sc)
obFn(mList)
```

### class neighbor()
**member vars:**
```
int size in [1 : inf]: 
float mutationP in [0, 1]: 
function mutationFunction: 
dict mutationConifg:
```

**usage:**
get mazes' neighbor
```
import test
import localSearch
mList = test.mazeFactory()
nebr = neighbor(size = 2, mutationP = 0.02)
newMaze = nebr(mList, validate = True)
```

## beamAnneal

### beamAnneal()
**input args:**
```
list maze with element frame.maze: init state maze
class localSearch.objectiveFunction obFn: evaluate maze score
class localSearch.neighbor nebr: generate maze's neighbor mazes
bool validate: 
	True: keep neighbors solvable; 
	False: much faster but prefroms worse
int teleportLimit in [2 : len(mList)*nebr.size]: max agent in one root; 
	0: auto-adapt; 
	1: no teleport permission
bool backTeleport: 
	True: record before-teleporting maze to be able to teleport back; 
	False: better is better, who cares losers
int maxIteration in [1 : inf]: directly halt searching
float temperature in [Tmin, inf]: control probability of simulated annealing, too small may cause early halt
float coolRate in [0 : 1]: control temperature decreasing speed. the larger, the slower. 
	1: disable simulate annealing
float minT in [0 : inf]: another way halt searching
int or float annealWeight in [0 : inf]: control probability of simulated annealing. the larger, the smaller.
int or float annealBias in [0 : inf]: control probability of simulated annealing, especially when no effective mutation. the larger, the smaller
int patience in [1 : inf]: the last way to halt searching when converged
float impatientRate in [0 : inf]: control the number of converged iteration to cause a halt. the larger, the fewer. 
	0: disable impatient converge halt
int tempSave in [1 : inf]: save temp result to disk every tempSave iters, including mList, temperature, patience. 
	0: no save
str savePath: saved file path. REMEMBER: end with a slash
```

**return val:**
```
list maze with element frame.maze: final state maze
```

**usage:**
```
import test
import localSearch as lS
import beamAnneal as bA
from solution import BFS
mList = test.mazeFactory(num = 6, size = 32, p = 0.4)
sF = BFS
sC = {'BDBFS' : True, 'quickGoal' : True, 'randomWalk' : True, 'checkFringe' : True}
obFn = lS.objectiveFunction(w = [0,1,0], solutionFunction = sF, solutionConfig = sC, deRandom = False)
nebr = lS.neighbor(size = 33, mutationP = 0.02)
sPath = 'D:/Users/endle/Desktop/520/log/'
newMaze = bA.beamAnneal(mList, obFn = obFn, nebr = nebr, teleportLimit = 2, maxIteration = 100, temperature = 10000., coolRate = 0.92, minT = 0.1, annealWeight = 16384, annealBias = 8, patience = 100, impatientRate = 0.001, tempSave = 10, savePath = sPath)
```

## Genetic Algorithm
### genetic.py
**usage:**
```
from genetic import Population

exampleAruguments = "{'mazeSize': 32, 'mazeWallRate': -1, 'populationSize': 750,'maxIteration': 130, 'reproductionRate': 0.7, 'mutationRate': 0.05, 'hugeMutation': 'True', 'weight': [0, 1, 0], 'solutionFunction': 'aStar', 'solutionConfig': {'LIFO': 'True', 'distFunction': 'manhattanDist'}}"

# Usage 1: The type of Arguments is string.
p1 = Population(**exampleArguments) 

# Usage 2: The type of Arguments is mapping.
#          Note that in 'solutionFunction' and 'disctFunction',
#          'aStar' and 'manhattanDist' should be enclose by apostrophe.
p2 = Population(mazeSize = 32, mazeWallRate = -1, populationSize = 50,
                       maxIteration = 100, reproductionRate = 0.7, mutationRate
                       = 0.05, hugeMutation = True, weight = [0, 1, 0],
                       solutionFunction = 'aStar', solutionConfig = {'LIFO':
                                                                     True,
                                                                     'distFunction'
                                                                     :
                                                                     'manhattanDist'})

finalChild, finalPopulation = p1.iterate() # finalChild is the hardest maze, finalPopulation is the population after the last iteration
```
**aruguments:**
```
mazeSize[2, inf]: The size of maze to be generated.
mazeWallRate[0.0, 1.0]: In each initial maze, the probability of each block to become a wall. The mazeWallRate will be randomly generated between [0.15, 0.38] if -1 is assigned to mazeWallRate.
populationSize[2, inf]: The size of mazes for each generation.
maxIteration[1, inf]: The max number of generations.
reproductionRate[0.0, 1.0]: Represents the percentage of how many individuals would have the chance to reproduce.
mutationRate[0.0, 1.0]: The probablity of the occurance of genetic mutation in a child.
hugeMutation[True or False]: Allow the child to have more than one block changed at one mutation. (Up to 0.5 * mazeSize ^ 2 blocks could be changed at one mutation. The number of blocks to be changed should be applied to normal distribution.(At least in my mind)) 
weight: You know... 
solutionFunction: Could be either 'aStar', 'BDAStar', 'BFS' and 'DFS'
solutionConfig: You know...
distFunction: Could be either 'euclideanDist', 'manhattanDist', 'chebyshevDist'
```

## alchemy
use genetic algorithm as pre-training and beam annealing as finetuning.
speaking of the result, god knows...

### getArg()
**input args:**
```
see previous description
```

**return val:**
```
dict gAArg, oFArg, nbArg, bAArg, alArg: input args for alchemy
```

### alchemy()
**input args:**
```
dict gAArg, bAArg:
class obFn nebr:
str logPath: used for save log mazes
int beamSeedNum in [1 : genetic.populationSize]: size of beam search
int nonPerfectSeedNum [0 : beamSeedNum]: the number of seed could be not enough good
```
**return val:**
```
list finalMaze with element frame.maze: finetuned mazes
```

**usage:**
maximize path length of aStar(manhattan)
```
#maze
mazeSize = 128 #test 16 first
mazeWallRate = -1
#genetic
populationSize = 500 #test 16 first
gAIteration = 130 #test 16 first
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
bAIteration = 200 #test 16 first
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
weight = [0, 1, 0] #path
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
test.saveMaze(finalMaze, resultPath, resultName)
```
*alternative*
weight:
```
weight = [1, 0, 0] #block
weight = [0, 1, 0] #path
weight = [0, 0, 1] #fringe
```
solution:
```
#DFS
solveFun = DFS
solveCfg = {'quickGoal' : True, 'randomWalk' : True} #CAUTION: should enable deRandom, see localSearch. TODO: improve genetic to enable deRandom
#BFS
solveFun = BFS
solveCfg = {'BDBFS' : True, 'quickGoal' : True, 'checkFringe' : True}
#AStar(euclidean)
solveFun = aStar
solveCfg = {'distFunction' : euclideanDist, 'LIFO' : True}
#AStar(manhattan)
solveFun = aStar
solveCfg = {'distFunction' : manhattanDist, 'LIFO' : True}
#AStar(chebyshev)
solveFun = aStar
solveCfg = {'distFunction' : chebyshevDist, 'LIFO' : True}
#BDAStar(euclidean)
solveFun = BDAStar
solveCfg = {'distFunction' : euclideanDist, 'LIFO' : True}
#BDAStar(manhattan)
solveFun = BDAStar
solveCfg = {'distFunction' : manhattanDist, 'LIFO' : True}
#BDAStar(chebyshev)
solveFun = BDAStar
solveCfg = {'distFunction' : chebyshevDist, 'LIFO' : True}
```