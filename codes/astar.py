import frame
import queue
import numpy as NP
import math
import solution

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

def aStar(m, distFunction = manhattanDist, LIFO = True):
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
    gscore = NP.full([size, size], NP.inf)
    lastPos = [NP.zeros([size, size], dtype = int), NP.zeros([size, size], dtype = int)]
    blockCount = 0
    goalPath = []
    routeLength = -1

    fringe.put(((distFunction(m.start, m.goal), blockCount), m.start, 0))
    gscore[0][0] = 0

    while not fringe.empty():
        current = fringe.get()
        stepcnt = current[2]
        x = current[1][0]
        y = current[1][1]
        if closed[x][y] > 0:
            continue
        closed[x][y] = 1
        if LIFO:
            blockCount -= 1
        else:
            blockCount += 1
        if current[1] == m.goal:
            tx = x
            ty = y
            for i in range(stepcnt):
                goalPath.append((tx, ty))
                tmp = lastPos[0][tx][ty]
                ty = lastPos[1][tx][ty]
                tx = tmp
            goalPath.append((0, 0))
            routeLength = len(goalPath)
            goalPath.reverse()
            break

        for i in range(4):
            nx = x + dir[i][0]
            ny = y + dir[i][1]
            nextPos = (nx, ny)
            if not isValid(m, size, nextPos):
                continue
            #if (closed[nx][ny] > 0 and stepcnt + 1 >= closed[nx][ny]):
            if closed[nx][ny] > 0:
                continue
            tg = 1 + gscore[x][y]
            if tg >= gscore[nx][ny]:
                continue
            gscore[nx][ny] = tg
            cost = tg + distFunction(nextPos, m.goal)
            fringe.put(((cost, blockCount), nextPos, stepcnt + 1))
            lastPos[0][nx][ny] = x
            lastPos[1][nx][ny] = y

    return (abs(blockCount), goalPath, routeLength)

if __name__ == '__main__':
    M = buildUp(size = 128, p = 0.35)
    t1 = aStar(m = M, distFunction = euclideanDist, LIFO = True)
    t2 = aStar(m = M, distFunction = euclideanDist, LIFO = False)
    t3 = aStar(m = M, distFunction = manhattanDist, LIFO = True)
    t4 = aStar(m = M, distFunction = manhattanDist, LIFO = False)
    t5 = aStar(m = M, distFunction = chebyshevDist, LIFO = True)
    t6 = aStar(m = M, distFunction = chebyshevDist, LIFO = False)
    t7 = solution.BFS(M, BDBFS = True, quickGoal = True, randomWalk = True, checkFringe = True)
    print(str(t1[0]) + ", " + str(t1[2]))
    print(str(t2[0]) + ", " + str(t2[2]))
    print(str(t3[0]) + ", " + str(t3[2]))
    print(str(t4[0]) + ", " + str(t4[2]))
    print(str(t5[0]) + ", " + str(t5[2]))
    print(str(t6[0]) + ", " + str(t6[2]))
    l = len(t7[1])
    print(str(t7[0]) + ", " + str(l))
    M.path = t1[1]
    imgastar = M.visualize()
    M.path = t7[1]
    imgbfs = M.visualize()
    imgastar.save('/home/shengjie/astar.png', 'PNG')
    imgbfs.save('/home/shengjie/bfs.png', 'PNG')
