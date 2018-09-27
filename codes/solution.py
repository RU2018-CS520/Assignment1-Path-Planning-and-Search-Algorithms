import frame
import numpy as np
import random
import itertools

def buildUp(size = 10, p = 0.2, initFunction = None, randomPosition = False):
	##int rows in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a block becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	m = frame.maze(rows = size, cols = size, p = p)
	m.build()
	return m


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


def DFS(m, IDDFS = False, keepSearch = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, checkFringe = False):
	#INPUT ARGS:
	#class maze m: maze to be solved
	#bool IDDFS: True: Iterative Deepening Depth First Search, promise optimal if updatable; False: DFS, much absolutely faster
	#bool keepSearch incompatible with quickGoal: True: not return until empty fringe, promise optimal if expand(updatable), works well with checkFringe; False: return as soon as goal, usually faster 
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe, in this case, DFS, effective and WITHOUT ANY COST; False: return when pop goal out from fringe
	#bool randomWalk: True: partially randomly pick a neighbor as next block, priority R and D > L and U, might works well; False: priority: strictly R > D > L > U, seems effective in this diagonal maze
	#bool randomWalkPlus: True: force randomWalk = True, totally random, no priority, may be effictive when randomPosition; False: depend on randomWalk
	#bool checkFringe: True: besides closed set, keep fringe distinct, to some extent, return a shorter path, but NOT DEFINITELY SHORTEST; False: just keep no back turning, a little bit faster
	#RETURN VALUE:
	#int blockCount in [1 : inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	#int maxDepth in [1 : inf]: the max depth of explored blocks
	
	def DFSCore(m, depthLimit = 0, keepSearch = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, checkFringe = False):
		#INPUT ARGS:
		#int depthLimit in [1 : inf]: used in IDDFS to limit depth each iteration explores, 0 if not IDDFS
		#OUTPUT ARGS: 
		#int maxDepth in [1 : inf]: max depth of searched blocks
		#others see DFS
		tempPath = []
		fringe = []
		closed = np.zeros_like(m.wall, dtype = np.uint32) #memory cost, but compatible with checkFringe #TODO: what if size > 65000
		blockCount = 0
		goalPath = []
		maxDepth = 0
		tempDepth = 0
		#init fringe
		fringe.extend(['pop',m.start])
		#core
		while fringe:
			temp = fringe.pop()
			#modify path to temp block
			if temp == 'pop':
				tempPath.pop()
				continue
			else:
				if checkFringe and closed[temp] != 0 and closed[temp] < len(tempPath) + 1:
					continue
				tempPath.append(temp)
				tempDepth = len(tempPath)
				if tempDepth > maxDepth:
					maxDepth = tempDepth
			#process block
			blockCount = blockCount + 1
			if temp == m.goal: #done
				if keepSearch and goalPath and len(goalPath) <= tempDepth: #keepSearch and path already exist and shorter
					continue
				#not keepSearch => first avilible path, or it have already returned; no path exist or longer path => update path
				goalPath = tempPath.copy() #hard copy
				depthLimit = len(goalPath) - 1
				if keepSearch:
					continue
				return (blockCount, goalPath, maxDepth)
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
						blockCount = blockCount + 1
						tempPath.append(m.goal)
						tempDepth = len(tempPath)
						if tempDepth > maxDepth:
							maxDepth = tempDepth
						goalPath = tempPath.copy() #hard copy
						return (blockCount, goalPath, maxDepth)
					if checkFringe:
						if closed[nextTemp] == 0 or closed[nextTemp] > tempDepth + 1:
							closed[nextTemp] = tempDepth + 1
						else:
							continue
					fringe.extend(['pop', nextTemp])
		#failed, no path
		return (blockCount, goalPath, maxDepth)

	#check input
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
		for depthLimit in itertools.count(1):
			count, path, maxDepth = DFSCore(m, depthLimit = depthLimit, quickGoal = quickGoal, randomWalk = randomWalk, randomWalkPlus = randomWalkPlus, checkFringe = checkFringe)
			totalCount = totalCount + count
			if path or maxDepth < depthLimit:
				return (totalCount, path, maxDepth)
	else:
		return DFSCore(m, keepSearch = keepSearch, quickGoal = quickGoal, randomWalk = randomWalk, randomWalkPlus = randomWalkPlus, checkFringe = checkFringe)


def BFS(m, BDBFS = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, checkFringe = False, depthLimit = 0):
	#INPUT ARGS:
	#class maze m: maze to be solved
	#bool BDBFS
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe, in this case, DFS, effective and WITHOUT ANY COST; False: return when pop goal out from fringe
	#bool randomWalk: True: partially randomly pick a neighbor as next block, priority R and D > L and U, might works well; False: priority: strictly R > D > L > U, seems effective in this diagonal maze
	#bool randomWalkPlus: True: force randomWalk = True, totally random, no priority, may be effictive when randomPosition; False: depend on randomWalk
	#bool checkFringe: True: besides closed set, keep fringe distinct, to some extent, return a shorter path, but NOT DEFINITELY SHORTEST; False: just keep no back turning, a little bit faster
	#int depthLimit in [1 : inf]: used to limit depth explores, 0 if n/a
	#RETURN VALUE:
	#int blockCount in [1 : inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	#int maxDepth in [1 : inf]: the max depth of explored blocks
	
	def getPath(temp, prev, goal):
		path = []
		while temp != goal:
			path.append(temp)
			temp = tuple(prev[temp])
		return path + [goal]

	sPath = []
	sFringe = []
	sClosed = np.zeros_like(m.wall, dtype = np.uint32)
	sPrev = np.full((m.wall.shape + (2,)), max(m.rows, m.cols), dtype = np.uint16) #TODO: size > 65000
	gPath = []
	gFringe = []
	gClosed = np.zeros_like(m.wall, dtype = np.uint32)
	gPrev = np.full((m.wall.shape + (2,)), max(m.rows, m.cols), dtype = np.uint16) #TODO: size > 65000
	blockCount = 0
	maxDepth = 0
	#init fringe
	sFringe.append(m.start)
	sPrev[m.start] = m.start
	gFringe.append(m.goal)
	gPrev[m.goal] = m.goal
	#prepare BDDFS
	tempPath = [sPath, gPath]
	fringe = [sFringe, gFringe]
	closed = [sClosed, gClosed]
	prev = [sPrev, gPrev]
	goal = [m.goal, m.start]
	if BDBFS:
		direction = 2
	else:
		direction = 1
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
				return (blockCount, sPath[:-1] + gPath, maxDepth)
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
							return (blockCount, sPath[:-1] + gPath, maxDepth)
					if checkFringe:
						if closed[i][nextTemp] == 0:
							closed[i][nextTemp] = closed[i][temp] + 1
						else:
							continue
					fringe[i].append(nextTemp)
					prev[i][nextTemp] = temp
	#failed, no path
	return (blockCount, sPath+gPath, maxDepth)


if __name__ == '__main__':
	M = buildUp(size = 7, p = 0.2)
	M.visualize()
	count, path, maxDepth = BFS(M, checkFringe = True)
	print(count)
	print(path)
	print(len(path))
	print(maxDepth)
