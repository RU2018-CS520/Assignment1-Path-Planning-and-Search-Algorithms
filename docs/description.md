# file description

## frame
a basic frame for MazeRunner, with class maze.

### class maze()
**member vars:**
```
int rows in [2 : inf]:
int cols in [2 : inf]:
float p in [0 : 1]:
np.array cell with ndim = 2:
list path with element (row, col): a path from S to G. None or [] if not exist
(row, col) start: start point, default (0, 0)
(row, col) goal: destination, default (rows-1, cols-1)
bool isBuilt: True: has built up walls, do NOT build it again; False: empty maze, call function build() before solove it
```

**member funcs:**
```
build(): build up walls, define maze.start and maze.goal
visualize(): plot maze map with path if exist.
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
solution.foo() #see solution description
if m.path:
	bar(m.path)
```

## solution
a number of algorithms to solve the maze, including Deep First Search, Breadth First Search, A* and their variants.

### DFS()