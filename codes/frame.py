import random
import numpy as np
from matplotlib import pyplot as plt

class maze(object):
	def __init__(self, rows = 10, cols = 10, initFunction = None, randomPosition = False):
		#int rows in [2: inf]: maze width
		#int cols in [2: inf]: maze height
		#function initFunction: init walls, None default trivalInit()
		#bool randomPosition: True: randomlize start and goal position; False: start at upper left and goal at lower right
		self.rows = rows
		self.cols = cols
		self.cell = np.zeros((rows, cols), dtype = np.uint8)
		self.path = None

		#init walls
		if initFunction is None:
			self.trivalInit()
		else:
			#TODO: process other init function
			pass

		#init S and G position
		if randomPosition is False:
			self.start = (0, 0)
			self.goal = (rows-1, cols-1)
			self.cell[self.start] = 0
			self.cell[self.goal] = 0
		else:
			#TODO: randomlize S and G
			pass


	def trivalInit(self, p = 0.2):
		#float p in [0 : 1]: probablity of a cell becomes a wall
		for row in range(self.rows):
			for col in range(self.cols):
				if random.random() < p:
					self.cell[row, col] = 1


	def visualize(self, size = 20, grid = 1, path = None):
		#int size in [0 : inf]: cell size(width and height)
		#int grid in [0 : size//2]: grid width
		#list path with elements of (row, col): a path from S to G. if not exist, input None
			
		def gridOn(image, size = 20, grid = 1, color = 128):
			#np.array image with ndim = 2: output maze map image
			#int color in [0 : 255]: grid color #TODO: adapt to chromatic image
			for row in range(self.rows):
				image[row*size : row*size+grid, :] = color
				image[row*size+size-grid : row*size+size, :] = color
				for col in range(self.cols):
					image[:, col*size : col*size+grid] = color
					image[:, col*size+size-grid : col*size+size] = color

		image = np.zeros((self.rows*size, self.cols*size), dtype = np.uint8) #TODO: adapt to chromatic image
		#grid
		if grid != 0:
			gridOn(image, size, grid, color = 64)
		#block
		for row in range(self.rows):
			for col in range(self.cols):
				if self.cell[row, col] == 1:
					image[row*size+grid : row*size+size-grid, col*size+grid : col*size+size-grid] = 255 #TODO: adapt to chromatic image
		#path
		if path is not None:
			#TODO: colorize path
			pass
		else:
			#start & goal
			sgColor = 32
			backColor = 0
			for cell in [self.start, self.goal]:
				image[cell[0]*size+grid : cell[0]*size+size-grid, cell[1]*size+grid : cell[1]*size+size-grid] = sgColor
				#break outer wall
				if cell[0] == 0: #first row, break wall U
					image[0 : grid, cell[1]*size+grid : cell[1]*size+size-grid] = backColor
				if cell[0] == self.rows-1: #last row, break wall D
					image[cell[0]*size+size-grid : cell[0]*size+size, cell[1]*size+grid : cell[1]*size+size-grid] = backColor
				if cell[1] == 0: #first col, break wall L
					image[cell[0]*size+grid : cell[0]*size+size-grid, 0 : grid] = backColor
				if cell[1] == self.cols-1: #last col, break wall R
					image[cell[0]*size+grid : cell[0]*size+size-grid, cell[1]*size+size-grid : cell[1]*size+size] = backColor
		#plot image
		plt.imshow(image, cmap = plt.cm.Greys, interpolation = 'none')
		plt.show()


if __name__ == '__main__':
	M = maze(10, 10, initFunction = None)
	M.visualize()