import frame
import queue
import numpy as NP
import math

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
    if m.cell[x][y] == 1:
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
 
def buildUp(size = 20, p = 0.2, initFunction = None, randomPosition = False):
	#int rows in [2 : inf]: maze width and height
	#float p in [0 : 1]: probablity of a cell becomes a wall
	#function initFunction: init walls, None default trivalInit()
	#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
	m = frame.maze(rows = size, cols = size, p = p)
	m.build()
	return m

def aStar(m, distType = 1):
    #INPUT ARGS:
	#class maze m: maze to be solved
    #int distType: a number indicating which method of distance calculation to use. aStar() will use Euclidean Distance as the distance if distType equals to 1, otherwise it will use Manhattan Distance.
	#RETURN VALUE:
	#int blockCount in [1, inf]: the number of blocks have opend
	#list goalPath with element (row, col): a path from S to G. [] if not exist
    #int routeLength: the length of the route from start to goal
    size = m.rows
    fringe = queue.PriorityQueue()
    closed = NP.zeros([size, size], dtype = int)
    lastPos = [NP.zeros([size, size], dtype = int), NP.zeros([size, size], dtype = int)]
    blockCount = 0
    goalPath = []
    routeLength = -1

    fringe.put((euclideanDist(m.start, m.goal), m.start, 0))

    while not fringe.empty():
        current = fringe.get()
        stepcnt = current[2]
        x = current[1][0]
        y = current[1][1]
        blockCount += 1
        if current[1] == m.goal:
            routeLength = stepcnt
            tx = x
            ty = y
            for i in range(stepcnt):
                goalPath.append((tx, ty))
                tmp = lastPos[0][tx][ty]
                ty = lastPos[1][tx][ty]
                tx = tmp
            goalPath.reverse()
            break

        for i in range(4):
            nx = x + dir[i][0]
            ny = y + dir[i][1]
            nextPos = (nx, ny)
            if not isValid(m, size, nextPos):
                continue
            if closed[nx][ny] == 1:
                continue
            closed[nx][ny] = 1
            if distType == 1:
                cost = euclideanDist(nextPos, m.goal) + current[0]
            else:
                cost = manhattanDist(nextPos, m.goal) + current[0]

            fringe.put((cost, nextPos, stepcnt + 1))
            lastPos[0][nx][ny] = x
            lastPos[1][nx][ny] = y

    return (blockCount, goalPath, routeLength)

if __name__ == '__main__':
    M = buildUp(size = 256, p = 0.2)
    t = aStar(m = M, distType = 1)
    t2 = aStar(m = M, distType = 2)
    print(t)
    print(t2)
    #M.visualize()
