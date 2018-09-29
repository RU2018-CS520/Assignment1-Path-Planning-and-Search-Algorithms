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
(row, col) start: start point, default (0, 0)
(row, col) goal: destination, default (rows-1, cols-1)
bool isBuilt: True: has built up walls, do NOT build it again; False: empty maze, call function build() before solove it
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
m.path = path
img = m.visualize(size = 10, grid = 1)
path = 'D:/Users/endle/Desktop/520/'
name = 'maze.png'
img.save(path+name, 'PNG')
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
bool keepSearch incompatible with quickGoal: 
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
		Caution: force randomWalk = True
	False: depend on randomWalk
bool checkFringe:
	True: besides closed set, keep fringe distinct. to some extent, return a shorter path, but not definitely shortest; 
		CAUTION: force expand(updatable = Ture)
	False: just keep no back turning. a little bit faster if not IDDFS
```
**return vals:**
```
int blockCount in [1 : inf]: The number of blocks have been opened. A reference of how hard the maze is.
list goalPath with element (row, col): a path from S to G. [] if not exist. REMEMBER: maze.path = goalPath
int maxDepth in [1 : inf]: the max depth of explored blocks, another way to measure how hard the maze is
```

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
		Caution: force randomWalk = True
	False: depend on randomWalk
bool checkFringe:
	True: besides closed set, keep fringe distinct. faster
	False: just keep no back turning.
int depthLimit in [1 : inf]: 
	used to limit depth explores, 0 if n/a
```

**return vals:**
```
int blockCount in [1 : inf]: The number of blocks have been opened. A reference of how hard the maze is.
list goalPath with element (row, col): a path from S to G. [] if not exist. REMEMBER: maze.path = goalPath
int maxDepth in [1 : inf]: the max depth of explored blocks, another way to measure how hard the maze is
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
```
**return vals**
```
int blockCount in [1 : inf]: The number of blocks have been opened. A reference of how hard the maze is.
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