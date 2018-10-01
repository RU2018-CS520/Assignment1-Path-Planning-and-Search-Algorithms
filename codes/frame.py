import random
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageChops

def setWall(maze, wall):
    maze.wall = wall
    return

class maze(object):
    def __init__(self, rows = 10, cols = 10, p = 0.2, rootNum = 0):
        #int rows in [2 : inf]: maze width
        #int cols in [2 : inf]: maze height
        #float p in [0 : 1]: probablity of a block becomes a wall
        self.rows = rows
        self.cols = cols
        self.p = p
        self.wall = np.zeros((rows, cols), dtype = np.bool)
        self.path = None
        self.isBuilt = False
        self.rootNum = rootNum
        self.solvable = False
        self.score = -1
        return

    def build(self, randomPosition = False, force = False, initFunction = None, initConifg = None):
        #function initFunction: init walls, None default trivalInit()
        #bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
        #bool force: True: force to rebuild maze; False: if maze.isBuilt immediately return original maze
        
        def trivalInit(maze):
            maze.wall = np.random.rand(maze.rows, maze.cols) < maze.p
            return

        if self.isBuilt:
            if force:
                self.wall = np.zeros_like(self.wall, dtype = np.bool)
            else:
                print('W: maze.build(), duplicate build')
                return
        #init walls
        if initFunction is None:
            trivalInit(self)
        elif initFunction is setWall:
            setWall(self, **initConifg)
        else:
            #TODO: process other init function
            pass
        #init S and G position
        if randomPosition is False:
            self.start = (0, 0)
            self.goal = (self.rows-1, self.cols-1)
            self.wall[self.start] = False
            self.wall[self.goal] = False
        else:
            #TODO: randomlize S and G
            pass
        self.isBuilt = True


    def visualize(self, size = 20, grid = 1, outerPath = None):
        #INPUT ARGS:
        #int size in [0 : inf]: block size(width and height)
        #int grid in [0 : size//2]: grid width
        #list outerPath with element (row, col): a path from S to G. None or [] if not exist
        #RETURN VALUE:
        #PIL.Image.Image img with mode = RGB: hi-res output maze map
            
        def gridOn(image, size = 20, grid = 1, color = 64, beacon = 128, distance = 16):
            #np.array image with ndim = 2: output maze map image
            #int color in [0 : 255]: grid color #TODO: adapt to chromatic image
            #int beacon in [0 : 255]: beacon gird for every 64 blocks
            for row in range(self.rows):
                if not bool(row%distance): #beacon
                    image[row*size : row*size+grid+1, :, :] = beacon
                    image[row*size+size-grid-1 : row*size+size, :, :] = beacon
                else:
                    image[row*size : row*size+grid+1, :, :] = color
                    image[row*size+size-grid-1 : row*size+size, :, :] = color

            for col in range(self.cols):
                if not bool(col%distance): #beacon
                    image[:, col*size : col*size+grid+1, :] = beacon
                    image[:, col*size+size-grid : col*size+size, :] = beacon
                else:
                    image[:, col*size : col*size+grid+1, :] = color
                    image[:, col*size+size-grid : col*size+size, :] = color

        if outerPath:
            path = outerPath
        else:
            path = self.path
        
        image = np.zeros((self.rows*size, self.cols*size, 3), dtype = np.uint8)
        #wall
        for row in range(self.rows):
            for col in range(self.cols):
                if self.wall[row, col]:
                    image[row*size+grid : row*size+size-grid, col*size+grid : col*size+size-grid] = 255
        #grid
        if grid != 0:
            gridOn(image, size, grid, color = 64)
        #path
        if path:
            sColor = [82, 172, 118]
            gColor = [195, 239, 172]
            beacon = [0, 0, 255]
            distance = 32
            rStart = sColor[0]
            gStart = sColor[1]
            bStart = sColor[2]
            rDist = gColor[0] - sColor[0]
            gDist = gColor[1] - sColor[1]
            bDist = gColor[2] - sColor[2]
            length = len(path)
            for i in range(length):
                row = path[i][0]
                col = path[i][1]
                if not bool(i%distance):
                    image[row*size : row*size+size, col*size : col*size+size] = (beacon[0], beacon[1], beacon[2] - (i//distance)*2)
                else:
                    image[row*size : row*size+size, col*size : col*size+size] = (rStart+i*rDist//length, gStart+i*gDist//length, bStart+i*bDist//length)
        else:
            #start & goal
            sgColor = [82, 172, 118]
            backColor = 0
            for block in [self.start, self.goal]:
                image[block[0]*size+grid : block[0]*size+size-grid, block[1]*size+grid : block[1]*size+size-grid, :] = sgColor
                #break outer wall
                if block[0] == 0: #first row, break wall U
                    image[0 : grid, block[1]*size+grid : block[1]*size+size-grid, :] = backColor
                if block[0] == self.rows-1: #last row, break wall D
                    image[block[0]*size+size-grid : block[0]*size+size, block[1]*size+grid : block[1]*size+size-grid, :] = backColor
                if block[1] == 0: #first col, break wall L
                    image[block[0]*size+grid : block[0]*size+size-grid, 0 : grid, :] = backColor
                if block[1] == self.cols-1: #last col, break wall R
                    image[block[0]*size+grid : block[0]*size+size-grid, block[1]*size+size-grid : block[1]*size+size, :] = backColor
        #plot image
        img = Image.fromarray(image) 
        img = ImageChops.invert(img)
        plt.imshow(img)
        plt.show() #TODO: non-block call
        return img

    def __lt__(self, other):
        return self.score > other.score


if __name__ == '__main__':
    M = maze(10, 10, 0.2)
    M.build()
    img = M.visualize()
    path = 'D:/Users/endle/Desktop/520/'
    name = 'maze.png'
#    img.save(path+name, 'PNG')
