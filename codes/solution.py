import frame

def buildUp(size = 10, initFunction = None, randomPosition = False):
	return frame.maze(rows = size, cols = size, initFunction = initFunction)

def DFS(m, IDDFS = False):
	path = []
	fringe = []
	closed = set()

	fringe.append(m.start)

	while fringe:
		temp = fringe.pop()
		if temp == 'pop':
			path.pop()
			continue
		else:
			path.append(temp)
			closed.add(temp)
		
		if temp == m.goal:
			return path

		tempFringe = []
		if temp[0] != 0 and m.cell[(temp[0]-1, temp[1])] != 1 and (temp[0]-1, temp[1]) not in closed: #L cell accessible
			tempFringe.append((temp[0]-1, temp[1]))
		if temp[0] != m.rows-1 and m.cell[(temp[0]+1, temp[1])] != 1 and (temp[0]+1, temp[1]) not in closed: #R cell accessible
			tempFringe.append((temp[0]+1, temp[1]))
		if temp[1] != 0 and m.cell[(temp[0], temp[1]-1)] != 1 and (temp[0], temp[1]-1) not in closed: #U cell accessible
			tempFringe.append((temp[0], temp[1]-1))
		if temp[1] != m.cols-1 and m.cell[(temp[0], temp[1]+1)] != 1 and (temp[0], temp[1]+1) not in closed: #D cell accessible
			tempFringe.append((temp[0], temp[1]+1))

		if tempFringe:
			for nextTemp in tempFringe:
				fringe.extend(['pop', nextTemp])


	return None

if __name__ == '__main__':
	M = buildUp()
	M.visualize()
	path = DFS(M)
	print(path)