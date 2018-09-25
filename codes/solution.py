import frame
import numpy as np
import random
import itertools

def buildUp(size = 10, p = 0.2, initFunction = None, randomPosition = False):
	##int rows in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a cell becomes a wall
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
	#int tempPath in [1 : inf]: length of tempPath, used to update fringe, use -1 if n/a
	#RETURN VALUE:
	#list tempFinge with element (row, col): accessible blocks
	row = temp[0]
	col = temp[1]
	#check if neighbor block is accessible
	tempFringeUL = []
	tempFringeDR = []
	#DO NOT CHANGE THE ORDER. r and d is prior than l and u in this diagonal maze
	if row != 0 and m.cell[row-1, col] != 1: #legal check
		if closed[row-1, col] == 0 or (updatable and closed[row-1, col] > tempPath): #unexplored or updatable
			tempFringeUL.append((row-1, col)) #U
	if col != 0 and m.cell[row, col-1] != 1: #legal check
		if closed[row, col-1] == 0 or (updatable and closed[row, col-1] > tempPath): #unexplored or updatable
			tempFringeUL.append((row, col-1)) #L
	if row != m.rows-1 and m.cell[row+1, col] != 1: #legal check
		if closed[row+1, col] == 0 or (updatable and closed[row+1, col] > tempPath): #unexplored or updatable
			tempFringeDR.append((row+1, col)) #D
	if col != m.cols-1 and m.cell[row, col+1] != 1: #legal check
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
	#bool IDDFS: True: Iterative Deepening Depth First Search, promise optimal; False: DFS, much faster
	#bool keepSearch incompatible with quickGoal: True: not return until empty fringe, promise optimal if expand(updatable), works well with checkFringe; False: return as soon as goal, usually faster 
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe, in this case, DFS, effective and WITHOUT ANY COST; False: return when pop goal out from fringe
	#bool randomWalk: True: partially randomly pick a neighbor as next block, priority R and D > L and U, might works well; False: priority: strictly R > D > L > U, seems effective in this diagonal maze
	#bool randomWalkPlus: True: force randomWalk = True, totally random, no priority, may be effictive when randomPosition; False: depend on randomWalk
	#bool checkFringe: True: besides closed set, keep fringe distinct, to some extent, return a shorter path, but NOT DEFINITELY SHORTEST; False: just keep no back turning, a little bit faster
	#RETURN VALUE:
	#int blockCount in [1, inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
	def DFSCore(m, depthLimit = 0, keepSearch = False, quickGoal = False, randomWalk = False, randomWalkPlus = False, checkFringe = False):
		#INPUT ARGS:
		#int depthLimit in [1 : inf]: used in IDDFS to limit depth each iteration explores, 0 if not IDDFS
		#OUTPUT ARGS: 
		#int maxDepth in [1 : inf]: max depth of searched blocks
		#others see DFS
		tempPath = []
		fringe = []
		closed = np.zeros_like(m.cell, dtype = np.uint16) #memory cost, but compatible with checkFringe #TODO: what if size > 250
		blockCount = 0
		goalPath = []
		maxDepth = 0
		tempDepth = 0
	
		fringe.extend(['pop',m.start])
	
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


if __name__ == '__main__':
	M = buildUp(size = 25, p = 0.2)
	M.visualize()
	count, path, maxDepth = DFS(M, IDDFS = True, checkFringe = True, randomWalkPlus = True)
	print(count)
	print(path)
	print(len(path))
	print(maxDepth)
