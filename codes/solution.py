import frame
import numpy as np

def buildUp(size = 20, p = 0.2, initFunction = None, randomPosition = False):
	##int rows in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a cell becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	m = frame.maze(rows = size, cols = size, p = p)
	m.build()
	return m


def expand(m, temp, closed):
	#class maze m: maze to be solved
	#(row, col) temp: temp processing block
	#np.array closed with ndim = 2: path length of each block in the maze, 0 if unexplored
	row = temp[0]
	col = temp[1]
	#check if neighbor block is accessible
	tempFringe = []
	#DO NOT CHANGE THE ORDER. r and d is prior than l and u in this diagonal maze
	if row != 0 and m.cell[row-1, col] != 1 and closed[row-1, col] == 0:
		tempFringe.append((row-1, col)) #U
	if col != 0 and m.cell[row, col-1] != 1 and closed[row, col-1] == 0:
		tempFringe.append((row, col-1)) #L
	if row != m.rows-1 and m.cell[row+1, col] != 1 and closed[row+1, col] == 0:
		tempFringe.append((row+1, col)) #D
	if col != m.cols-1 and m.cell[row, col+1] != 1 and closed[row, col+1] == 0:
		tempFringe.append((row, col+1)) #R
	return tempFringe

def DFS(m, IDDFS = False, keepSearch = False, quickGoal = False, randomWalk = False, checkFringe = False):
	#class maze m: maze to be solved
	#bool IDDFS: True: Iterative Deepening Depth First Search, promise optimal; False: DFS, much faster
	#bool keepSearch incompatible with quickGoal: True: not return until empty fringe, promise optimal; False: return as soon as goal, usually faster 
	#bool quickGoal incompatible with keepSearch: True: immediately return when push goal into fringe, in this case, DFS, effective and WITHOUT ANY COST; False: return when pop goal out from fringe
	#bool randomWalk: True: randomly pick a neighbor as next block, might work well with randomPosition; False: priority: R > D > L > U, seems effective in this diagonal maze
	#bool checkFringe: True: besides closed set, keep fringe distinct, to some extent, return a shorter path, but NOT DEFINITELY SHORTEST; False: just keep no back turning, a little bit faster
	def DFSCore(m, keepSearch = False, quickGoal = False, randomWalk = False, checkFringe = False):
		#see DFS
		path = []
		fringe = []
		closed = np.zeros_like(m.cell, dtype = np.uint8)
	
		fringe.append(m.start)
	
		while fringe:
			temp = fringe.pop()
			if temp == 'pop':
				path.pop()
				continue
			else:
				path.append(temp)
				closed[temp] = len(path)
			
			if temp == m.goal:
				return path
	
			tempFringe = expand(m, temp, closed)
	
			if tempFringe:
				for nextTemp in tempFringe:
					fringe.extend(['pop', nextTemp])
	
		return None

	if IDDFS:
		#TODO: IDDFS
		pass
	else:
		return DFSCore(m, keepSearch = False, quickGoal = False, randomWalk = False, checkFringe = False)


if __name__ == '__main__':
	M = buildUp()
	M.visualize()
	path = DFS(M)
	print(path)