import frame
import numpy as np
import random
import itertools

#init maze
def buildUp(size = 10, p = 0.2, initFunction = None, randomPosition = False, force = False):
	##int size in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a block becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	#bool force: True: force to rebuild maze; False: if maze.isBuilt immediately return original maze
	m = frame.maze(rows = size, cols = size, p = p)
	m.build(initFunction = initFunction, randomPosition = randomPosition, force = force)
	return m

#explore temp's neighbor
def expand(m, temp, closed, randomWalk = True, updatable = False, tempPath = -1):
	#INPUT ARGS:
	#class maze m: maze to be solved
	#(row, col) temp: temp processing block
	#np.array closed with ndim = 2: path length of each block in the maze, 0 if unexplored
	#bool randomWalk: True: partially randomly pick a neighbor as next block, priority R and D > L and U, might works well; False: priority: strictly R > D > L > U, seems effective in this diagonal maze
	#bool updatable: True: enable closed set to update, force True if keepSearch or checkFringe; False: closed blocks will never open again, save a huge amount of time
	#int tempPath in [1 : inf]: length of tempPath, used when updatable, use -1 if n/a
	#RETURN VALUE:
	#list tempFringe with element (row, col): accessible blocks
	row = temp[0]
	col = temp[1]
	#check if neighbor block is accessible
	tempFringeUL = []
	tempFringeDR = []
	#DO NOT CHANGE THE ORDER. r and d is prior than l and u in this diagonal maze
	if row != 0 and not m.wall[row-1, col]: #legal check
		if closed[row-1, col] == 0 or (updatable and closed[row-1, col] > tempPath): #unexplored or updatable
			tempFringeUL.append((row-1, col)) #U
	if col != 0 and not m.wall[row, col-1]: #legal check
		if closed[row, col-1] == 0 or (updatable and closed[row, col-1] > tempPath): #unexplored or updatable
			tempFringeUL.append((row, col-1)) #L
	if row != m.rows-1 and not m.wall[row+1, col]: #legal check
		if closed[row+1, col] == 0 or (updatable and closed[row+1, col] > tempPath): #unexplored or updatable
			tempFringeDR.append((row+1, col)) #D
	if col != m.cols-1 and not m.wall[row, col+1]: #legal check
		if closed[row, col+1] == 0 or (updatable and closed[row, col+1] > tempPath): #unexplored or updatable
			tempFringeDR.append((row, col+1)) #R
	#respectively shuffle
	if randomWalk:
		random.shuffle(tempFringeUL)
		random.shuffle(tempFringeDR)
	return tempFringeUL + tempFringeDR

def getPath(temp, prev, start):
	#INPUT ARGS:
	#(row, col) temp: temp processing block
	#np.array prev with ndim = 2: record temp's prev block (row, col). (m.rows, m.cols) if n/a
	#(row, col) start: path's start block
	#RETURN VALUE:
	#list path with element (row, col): a path from temp to S.
	path = []
	while temp != start:
		path.append(temp)
		temp = tuple(prev[temp])
	return path + [start]


def DFS(m, IDDFS = False, keepSearch = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, distinctFringe = False, checkFringe = False, plotClosed = False):
	#INPUT ARGS: #further reading: description.md
	#class maze m: maze to be solved
	#bool IDDFS: True: Iterative Deepening Depth First Search; False: DFS
	#bool keepSearch incompatible with quickGoal, distinctFringe: True: not return until empty fringe; False: return as soon as goal, usually faster 
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe; False: return when pop goal out from fringe
	#bool randomWalk: True: priority: R and D > L and U; False: priority: strictly R > D > L > U
	#bool randomWalkPlus: True: totally random, no priority; False: depend on randomWalk
	#bool distinctFringe imcompatible with checkFringe, keepSearch: True: keep fringe distinct, and closed block will be always closed; False: just keep no back turning, but can visit a block twice
	#bool checkFringe imcompatible with distinctFringe: True: keep fringe distinct and best; False: just keep no back turning, but can visit a block twice
	#bool plotClosed: True: pass closed set to maze for ploting; False: discard closed set
	#RETURN VALUE:
	#int blockCount in [1 : inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	#int maxDepth in [1 : inf]: the max depth of explored blocks
	
	def DFSCore(m, IDDFS = False, depthLimit = 0, keepSearch = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, distinctFringe = False, checkFringe = False, plotClosed = False):
		#INPUT ARGS:
		#int depthLimit in [1 : inf]: used in IDDFS to limit depth each iteration explores, 0 if not IDDFS
		#OUTPUT ARGS: 
		#int maxDepth in [1 : inf]: max depth of searched blocks
		#others see DFS
		fringe = []
		visited = np.zeros_like(m.wall, dtype = np.bool)
		closed = np.zeros_like(m.wall, dtype = np.uint32) #memory cost, but compatible with checkFringe #TODO: what if size > 65000
		prev = np.full((m.wall.shape + (2,)), max(m.rows, m.cols), dtype = np.uint16) #TODO: size > 65000
		prev[m.start] = m.start
		blockCount = 0
		goalPath = []
		maxDepth = 0
		tempDepth = 0
		maxFirngeSize = 1
		#init fringe
		fringe.append((m.start, 1))
		#core
		while fringe:
			temp, tempDepth = fringe.pop()
			#preprocessing
			if distinctFringe:
				if visited[temp]:
					continue
				else:
					visited[temp] = True
			if checkFringe and closed[temp] != 0 and closed[temp] < tempDepth:
				continue
			if tempDepth > maxDepth:
				maxDepth = tempDepth
			#process block
			blockCount = blockCount + 1
			if temp == m.goal: #done
				if keepSearch and goalPath and len(goalPath) <= tempDepth: #keepSearch and path already exist and shorter
					continue
				#not keepSearch => first avilible path, or it have already returned; no path exist or longer path => update path
				goalPath = getPath(temp, prev, m.start) #hard copy
				goalPath.reverse()
				depthLimit = len(goalPath) - 1 #no need to search deeper blocks
				if keepSearch:
					continue
				if plotClosed:
					m.closed = closed.astype(np.bool)
				if IDDFS:
					return (blockCount, goalPath, maxFirngeSize, maxDepth)
				return (blockCount, goalPath, maxFirngeSize)
			else:
				closed[temp] = tempDepth
			#expand block
			if depthLimit and tempDepth >= depthLimit:
				continue
			tempFringe = expand(m, temp, closed, randomWalk = randomWalk and not randomWalkPlus, updatable = keepSearch or checkFringe, tempPath = tempDepth)
			#push into fringe
			if tempFringe:
				if randomWalkPlus:
					random.shuffle(tempFringe)
				for nextTemp in tempFringe:
					if quickGoal and nextTemp == m.goal:
						prev[nextTemp] = temp
						blockCount = blockCount + 1
						if tempDepth+1 > maxDepth:
							maxDepth = tempDepth+1
						goalPath = getPath(nextTemp, prev, m.start)
						goalPath.reverse()
						if plotClosed:
							m.closed = closed.astype(np.bool)
						if IDDFS:
							return (blockCount, goalPath, maxFirngeSize, maxDepth)
						return (blockCount, goalPath, maxFirngeSize)
					if checkFringe:
						if closed[nextTemp] == 0 or closed[nextTemp] > tempDepth + 1:
							closed[nextTemp] = tempDepth + 1
						else:
							continue
					prev[nextTemp] = temp
					fringe.append((nextTemp, tempDepth+1))
			if len(fringe) > maxFirngeSize:
				maxFirngeSize = len(fringe)
		#failed, no path
		if plotClosed:
			m.closed = closed.astype(np.bool)
		if IDDFS:
			return (blockCount, goalPath, maxFirngeSize, maxDepth)
		return (blockCount, goalPath, maxFirngeSize)

	#check input
	if keepSearch and distinctFringe:
		print('W: DFS(), contradictory input args DISTINCTFRINGE and KEEPSEARCH')
		keepSearch = checkFringe
		distinctFringe = False
	if distinctFringe and checkFringe:
		print('W: DFS(), contradictory input args DISTINCTFRINGE and CHECKFRINGE')
		distinctFringe = False
		checkFringe = False
	if IDDFS and keepSearch:
		print('W: DFS(), contradictory input args IDDFS and KEEPSEARCH')
		keepSearch = False
	if keepSearch and quickGoal:
		print('W: DFS(), contradictory input args KEEPSEARCH and QUICKGOAL')
		keepSearch = checkFringe
		quickGoal = False
	#core
	if IDDFS:
		totalCount = 0
		prevCount = 0
		for depthLimit in itertools.count(1):
			count, path, maxFirngeSize, maxDepth = DFSCore(m, IDDFS = IDDFS, depthLimit = depthLimit, quickGoal = quickGoal, randomWalk = randomWalk, randomWalkPlus = randomWalkPlus, distinctFringe = distinctFringe, checkFringe = checkFringe, plotClosed = plotClosed)
			totalCount = totalCount + count
			if path or maxDepth < depthLimit:
				return (totalCount, path, maxFirngeSize)
	else:
		return DFSCore(m, keepSearch = keepSearch, quickGoal = quickGoal, randomWalk = randomWalk, randomWalkPlus = randomWalkPlus, distinctFringe = distinctFringe, checkFringe = checkFringe, plotClosed = plotClosed)


def BFS(m, BDBFS = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, checkFringe = False, depthLimit = 0, plotClosed = False):
	#INPUT ARGS:
	#class maze m: maze to be solved
	#bool BDBFS: True: BiDirectional Breadth First Search; False: BFS
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe; False: return when pop goal out from fringe
	#bool randomWalk: True: priority: R and D > L and U; False: priority: strictly R > D > L > U
	#bool randomWalkPlus: True: totally random, no priority; False: depend on randomWalk
	#bool checkFringe: True: keep fringe distinct; False: just keep no back turning
	#int depthLimit in [1 : inf]: used to limit depth explores, 0 if n/a
	#bool plotClosed: True: pass closed set to maze for ploting; False: discard closed set
	#RETURN VALUE:
	#int blockCount in [1 : inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	#int maxDepth in [1 : inf]: the max depth of explored blocks

	sPath = []
	sFringe = []
	sClosed = np.zeros_like(m.wall, dtype = np.uint32)
	sPrev = np.full((m.wall.shape + (2,)), max(m.rows, m.cols), dtype = np.uint16) #TODO: size > 65000
	sFringeSize = 1
	gPath = []
	gFringe = []
	gClosed = np.zeros_like(m.wall, dtype = np.uint32)
	gPrev = np.full((m.wall.shape + (2,)), max(m.rows, m.cols), dtype = np.uint16) #TODO: size > 65000
	gFringeSize = 1
	blockCount = 0
	maxDepth = 0
	maxFirngeSize = 2
	#init fringe
	sFringe.append(m.start)
	sPrev[m.start] = m.start
	gFringe.append(m.goal)
	gPrev[m.goal] = m.goal
	#prepare BDBFS
	tempPath = [sPath, gPath]
	fringe = [sFringe, gFringe]
	closed = [sClosed, gClosed]
	prev = [sPrev, gPrev]
	goal = [m.goal, m.start]
	fringeSize = [sFringeSize, gFringeSize]
	direction = 1 + int(BDBFS)
	#core
	while sFringe and gFringe:
		for i in range(direction):
			temp = fringe[i].pop(0)
			#process block
			blockCount = blockCount + 1
			if temp == goal[i] or closed[i-1][temp] != 0: #done
				sPath = getPath(temp, prev[0], goal[1])
				gPath = getPath(temp, prev[1], goal[0])
				sPath.reverse()
				if not BDBFS:
					maxDepth = maxDepth + 1
				if plotClosed:
					m.closed = sClosed.astype(np.bool) | gClosed.astype(np.bool) 
				return (blockCount, sPath[:-1] + gPath, maxFirngeSize - int(not BDBFS))
			else:
				closed[i][temp] = closed[i][tuple(prev[i][temp])] + 1
				if closed[i][temp] > maxDepth:
					maxDepth = closed[i][temp]
			#expand block
			if depthLimit and closed[i][temp] >= depthLimit:
				continue
			tempFringe = expand(m, temp, closed[i], randomWalk = randomWalk and not randomWalkPlus, updatable = False, tempPath = closed[i][temp])
			#push into fringe
			if tempFringe:
				if randomWalkPlus:
					random.shuffle(tempFringe)
				if i == 1: #goal side
					tempFringe.reverse()
				for nextTemp in tempFringe:
					if quickGoal:
						if nextTemp == goal[i] or closed[i-1][nextTemp] != 0:
							blockCount = blockCount + 1
							prev[i][nextTemp] = temp
							sPath = getPath(nextTemp, prev[0], goal[1])
							gPath = getPath(nextTemp, prev[1], goal[0])
							sPath.reverse()
							if not BDBFS:
								maxDepth = maxDepth + 1
							if plotClosed:
								m.closed = sClosed.astype(np.bool) | gClosed.astype(np.bool)
							return (blockCount, sPath[:-1] + gPath, maxFirngeSize - int(not BDBFS))
					if checkFringe:
						if closed[i][nextTemp] == 0:
							closed[i][nextTemp] = closed[i][temp] + 1
						else:
							continue
					fringe[i].append(nextTemp)
					prev[i][nextTemp] = temp
			#update fringe size
			fringeSize[i] = len(fringe[i])
			if fringeSize[0] + fringeSize[1] > maxFirngeSize:
				maxFirngeSize = fringeSize[0] + fringeSize[1]
	#failed, no path
	if plotClosed:
		m.closed = sClosed.astype(np.bool) | gClosed.astype(np.bool)
	return (blockCount, sPath + gPath, maxFirngeSize - int(not BDBFS))


if __name__ == '__main__':
	M = buildUp(size = 128, p = 0.3)
	M.visualize(size = 20)
	count, path, maxFirnge = DFS(M, quickGoal = True, randomWalk = False, checkFringe = False, plotClosed = True)
	print(count)
	print(path)
	print(len(path))
	print(maxFirnge)
	M.path = path
	img = M.visualize()
	# count, path, maxFirnge = DFS(M, quickGoal = True, randomWalk = True)
	# print(count)
	# print(path)
	# print(len(path))
	# print(maxFirnge)
	# M.path = path
	# img = M.visualize()
	# path = 'D:/Users/endle/Desktop/520/'
	# name = 'maze.png'
#	img.save(path+name, 'PNG')