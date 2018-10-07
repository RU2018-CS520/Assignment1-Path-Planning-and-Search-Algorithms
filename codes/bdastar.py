import frame
import queue
import numpy as NP
import math
import solution
import astar

dir = [[-1, 0], [1, 0], [0, -1], [0, 1]] #directions of moving, respectively up, down, left, right

def isValid(m, size, nextPos):
	#to judge if nextPos is accessible
	#INPUT ARGS:
	#m: the maze to be solved
	#size: the size of the maze
	#nextPos: next step of the agent
	x = int(nextPos[0])
	y = int(nextPos[1])
	if x < 0 or y < 0 or x >= size or y >= size:
		return False
	if m.wall[x][y]:
		return False
	return True

def euclideanDist(u, v):
	x1 = u[0]
	y1 = u[1]
	x2 = v[0]
	y2 = v[1]
	return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def manhattanDist(u, v):
	x1 = u[0]
	y1 = u[1]
	x2 = v[0]
	y2 = v[1]
	return abs(x1 - x2) + abs(y1 - y2)

def chebyshevDist(u, v):
	x1 = u[0]
	y1 = u[1]
	x2 = v[0]
	y2 = v[1]
	return max(abs(x1 - x2), abs(y1 - y2))
 
def buildUp(size = 20, p = 0.2, initFunction = None, randomPosition = False):
	#int rows in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a block becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	m = frame.maze(rows = size, cols = size, p = p)
	m.build()
	return m

def biDirectionalAStar(m, distFunction = manhattanDist, LIFO = True, plotClosed = False):
	#INPUT ARGS:
	#class maze m: maze to be solved
	#int distType: a number indicating which method of distance calculation to use. aStar() will use Euclidean Distance as the distance if distType equals to 1, otherwise it will use Manhattan Distance.
	#bool plotClosed: True: pass closed set to maze for ploting; False: discard closed set
	#RETURN VALUE:
	#int blockCount in [1, inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	#int maxFringeSize in [1, inf]: the max size of fringe
	size = m.rows
	sFringe = queue.PriorityQueue()
	gFringe = queue.PriorityQueue()
	sVisited = NP.zeros_like(m.wall, dtype = NP.bool)
	gVisited = NP.zeros_like(m.wall, dtype = NP.bool)
	sClosed = NP.zeros_like(m.wall, dtype = NP.uint32)
	gClosed = NP.zeros_like(m.wall, dtype = NP.uint32)
	sLastPos = NP.zeros([m.rows, m.cols, 2], dtype = NP.uint16)
	gLastPos = NP.zeros([m.rows, m.cols, 2], dtype = NP.uint16)
	sLastPos[m.start] = m.goal #uesd to identify the end of a path when generate
	gLastPos[m.goal] = m.start #uesd to identify the end of a path when generate
	blockCount = 0
	sGoalPath = []
	gGoalPath = []
	fullGoalPath = []
	routeLength = 0
	doneFlag = False
	maxFringeSize = 2

	sFringe.put(((distFunction(m.start, m.goal), blockCount), m.start, 1))
	gFringe.put(((distFunction(m.goal, m.start), blockCount), m.goal, 1))
	#prepare for BD
	fringe = [sFringe, gFringe]
	visited = [sVisited, gVisited]
	closed = [sClosed, gClosed]
	lastPos = [sLastPos, gLastPos]
	goalPath = [sGoalPath, gGoalPath]
	goal = [m.goal, m.start]

	while not sFringe.empty() and not gFringe.empty() and not doneFlag:
		for d in range(2):
			current = fringe[d].get()
			stepcnt = current[2]
			x = current[1][0]
			y = current[1][1]
			
			if visited[d][x][y] == True:
				continue
			visited[d][x][y] = True

			closed[d][x, y] = stepcnt
			if LIFO:
				blockCount -= 1
			else:
				blockCount += 1
			if current[1] == goal[d] or closed[d-1][current[1]] != 0:
				for direction in range(2):
					tx = x
					ty = y
					while (tx, ty) != goal[direction]:
						goalPath[direction].append((tx, ty))
						tx, ty = lastPos[direction][tx, ty]
				sGoalPath.reverse()
				fullGoalPath = sGoalPath[:-1] + gGoalPath
				routeLength = len(fullGoalPath)
				doneFlag = True
				break
	
			for i in range(4):
				nx = x + dir[i][0]
				ny = y + dir[i][1]
				nextPos = (nx, ny)
				if not isValid(m, size, nextPos):
					continue
				if closed[d][nx, ny] > 0 and stepcnt + 1 >= closed[d][nx, ny]:
					continue
				closed[d][nx, ny] = stepcnt + 1
				cost = distFunction(nextPos, goal[d]) + stepcnt + 1
				fringe[d].put(((cost, blockCount), nextPos, stepcnt + 1))
				lastPos[d][nx, ny] = (x, y)
			#update fringe size
			fringeSize = sFringe.qsize() + gFringe.qsize()
			if fringeSize > maxFringeSize:
				maxFringeSize = fringeSize
	if plotClosed:
		m.closed = sClosed.astype(NP.bool) | gClosed.astype(NP.bool)
	return (abs(blockCount), fullGoalPath, maxFringeSize)

if __name__ == '__main__':
	M = buildUp(size = 64, p = 0.35)
	t1 = biDirectionalAStar(m = M, distFunction = euclideanDist, LIFO = True, plotClosed = True)
	t3 = biDirectionalAStar(m = M, distFunction = manhattanDist, LIFO = True)
	t5 = biDirectionalAStar(m = M, distFunction = chebyshevDist, LIFO = True)
	t7 = solution.BFS(M, BDBFS = True, quickGoal = True, randomWalk = True, checkFringe = True)
	t9 = astar.aStar(m = M, distFunction = chebyshevDist, LIFO = True)
	print(str(t1[0]) + ", " + str(t1[2]))

	print(str(t3[0]) + ", " + str(t3[2]))

	print(str(t5[0]) + ", " + str(t5[2]))

	l = len(t7[1])
	print(str(t7[0]) + ", " + str(l))
	print(str(t9[0]) + ", " + str(t9[2]))
	M.path = t3[1]
	imgastar = M.visualize()
	M.path = t7[1]
#	imgbfs = M.visualize()
#	imgastar.save('/home/shengjie/astar.png', 'PNG')
#	imgbfs.save('/home/shengjie/bfs.png', 'PNG')
