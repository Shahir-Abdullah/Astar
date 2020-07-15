import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import math as m

MAX = 100
heuristic_option = 0
# plot map and path
def draw_map(grid, start_node, goal_node, path=None):
    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(grid)
    ax.scatter(start_node[1],start_node[0], marker = "*", color = "green", s = 200)
    ax.scatter(goal_node[1],goal_node[0], marker = "*", color = "red", s = 200)

    if path != None:
        x_coords = []
        y_coords = []

        for i in (range(0,len(path))):
            x = path[i][0]
            y = path[i][1]
            x_coords.append(x)
            y_coords.append(y)

        #plot the path

        ax.plot(y_coords,x_coords, color = "black")
        plt.show()
        plt.show()

class Pair(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class OpenListElement(object):
	def __init__(self, f, pair):
		self.f = f
		self.x = pair.x
		self.y = pair.y


class Cell(object):
	def __init__(self, px, py, f, g, h):
		self.parent_x = px
		self.parent_y = py
		self.f = f
		self.g = g
		self.h = h


def validCell(row, col):
	if row >= 0 and row <= 7 and col >= 0 and col <= 7:
		return True
	else:
		return False


def cellBlocked(grid, row, col):
	if grid[row][col] == 0:
		return True
	else:
		return False


def isDestination(row, col, dest):  # dest is Pair object
	if row == dest.x and col == dest.y:
		return True
	else:
		return False


def heuristic_manhattan(row, col, dest):
	return (abs(row-dest.x) + abs(col-dest.y))


def heuristic_diagonal(row, col, dest):
	return max(abs(row-dest.x), abs(col-dest.y))


def heuristic_euclidian(row, col, dest):
	return m.sqrt((row-dest.x)**2 + (col-dest.y)**2)


def showPath(cellInfo, dest):
	print('The path is ')
	row = dest.x
	col = dest.y
	path = []
	while cellInfo[row][col].parent_x != row or cellInfo[row][col].parent_y != col:
		path.append(Pair(row, col))
		tr = cellInfo[row][col].parent_x
		tc = cellInfo[row][col].parent_y
		row = tr
		col = tc
	path.append(Pair(row, col))
	copypath = []
	
	while path:
		p = path[-1]
		path.pop()
		copypath.append((p.x, p.y))
		print('-> ', '(', p.x, p.y, ')')

	return copypath


def aStarSearch(grid, src, dest):
	if validCell(src.x, src.y) == False:
		print('Invalid source')
		return
	if validCell(dest.x, dest.y) == False:
		print('Invalid destination')
		return
	if cellBlocked(grid, src.x, src.y) or cellBlocked(grid, dest.x, dest.y):
		print('Source or destination is blocked')
		return
	if isDestination(src.x, src.y, dest):
		print('We are already at the destination')
		return

	# closed list for cell checking 0 means unchecked 1 for checked
	closedList = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0]
	]
	# initializing cellInfo
	cellInfo = []
	for i in range(8):
		cellrow = []
		for j in range(8):
			c1 = Cell(-1, -1, MAX, MAX, MAX)
			cellrow.append(c1)
		cellInfo.append(cellrow)
	# initialize the source node
	i = src.x
	j = src.y
	cellInfo[i][j].f = 0
	cellInfo[i][j].g = 0
	cellInfo[i][j].h = 0
	cellInfo[i][j].parent_x = i
	cellInfo[i][j].parent_y = j

	# creating an open list containing OpenListElement objects
	openList = []
	openList.append(OpenListElement(0.0, Pair(i, j)))

	foundDest = False

	while openList:
		p = openList[0]
		del openList[0]
		i = p.x
		j = p.y
		closedList[i][j] = 1

	    # generating the NSWE successors of this cell

	   	# North successor
		if validCell(i-1, j) == True:
			if isDestination(i-1, j, dest) == True:
			   cellInfo[i-1][j].parent_x = i
			   cellInfo[i-1][j].parent_y = j
			   print('Destination cell is found\n')
			   path = showPath(cellInfo, dest)
			   foundDest = True

			   return path 

			elif closedList[i-1][j] == 0 and cellBlocked(grid, i-1, j) == False:

				gNew = cellInfo[i][j].g + 1.0 
				hNew = 0
				if heuristic_option == 0:
					hNew = heuristic_euclidian(i-1, j, dest) 
				elif heuristic_option == 1:
					hNew = heuristic_diagonal(i-1, j, dest)
				else:
					hNew = heuristic_manhattan(i-1, j, dest)
				
				fNew = gNew + hNew 

				if cellInfo[i-1][j].f == MAX or cellInfo[i-1][j].f > fNew:
					openList.append(OpenListElement(fNew, Pair(i-1, j)))
					cellInfo[i-1][j].f = fNew 
					cellInfo[i-1][j].g = gNew
					cellInfo[i-1][j].h = hNew  
					cellInfo[i-1][j].parent_x = i 
					cellInfo[i-1][j].parent_y = j		
		# south successor 
		if validCell(i+1, j) == True:
			if isDestination(i+1, j, dest) == True:
			   cellInfo[i+1][j].parent_x = i
			   cellInfo[i+1][j].parent_y = j
			   print('Destination cell is found\n')
			   path = showPath(cellInfo, dest)
			   foundDest = True 
			   return path 
		
			elif closedList[i+1][j] == 0 and cellBlocked(grid, i+1, j) == False:
				gNew = cellInfo[i][j].g + 1.0 
				hNew = 0
				if heuristic_option == 0:
					hNew = heuristic_euclidian(i+1, j, dest)  
				elif heuristic_option == 1:
					hNew = heuristic_diagonal(i+1, j, dest)
				else:
					hNew = heuristic_manhattan(i+1, j, dest)
				
				fNew = gNew + hNew 

				if cellInfo[i+1][j].f == MAX or cellInfo[i+1][j].f > fNew:
					openList.append(OpenListElement(fNew, Pair(i+1, j)))
					cellInfo[i+1][j].f = fNew 
					cellInfo[i+1][j].g = gNew
					cellInfo[i+1][j].h = hNew  
					cellInfo[i+1][j].parent_x = i 
					cellInfo[i+1][j].parent_y = j
		# east successor 
		if validCell(i, j+1) == True:
			if isDestination(i, j+1, dest) == True:
			   cellInfo[i][j+1].parent_x = i
			   cellInfo[i][j+1].parent_y = j
			   print('Destination cell is found\n')
			   path = showPath(cellInfo, dest)
			   foundDest = True 
			   return path 
		
			elif closedList[i][j+1] == 0 and cellBlocked(grid, i, j+1) == False:
				gNew = cellInfo[i][j].g + 1.0 
				hNew = 0
				if heuristic_option == 0:
					hNew = heuristic_euclidian(i, j+1, dest)  
				elif heuristic_option == 1:
					hNew = heuristic_diagonal(i, j+1, dest)
				else:
					hNew = heuristic_manhattan(i, j+1, dest) 
				fNew = gNew + hNew 

				if cellInfo[i][j+1].f == MAX or cellInfo[i][j+1].f > fNew:
					openList.append(OpenListElement(fNew, Pair(i, j+1)))
					cellInfo[i][j+1].f = fNew 
					cellInfo[i][j+1].g = gNew
					cellInfo[i][j+1].h = hNew  
					cellInfo[i][j+1].parent_x = i 
					cellInfo[i][j+1].parent_y = j
		# wast successor 
		if validCell(i, j-1) == True:
			if isDestination(i, j-1, dest) == True:
			   cellInfo[i][j-1].parent_x = i
			   cellInfo[i][j-1].parent_y = j
			   print('Destination cell is found\n')
			   path = showPath(cellInfo, dest)
			   foundDest = True 
			   return path 
		
			elif closedList[i][j-1] == 0 and cellBlocked(grid, i, j-1) == False:
				gNew = cellInfo[i][j].g + 1.0 
				hNew = 0
				if heuristic_option == 0:
					hNew = heuristic_euclidian(i, j-1, dest)  
				elif heuristic_option == 1:
					hNew = heuristic_diagonal(i, j-1, dest)
				else:
					hNew = heuristic_manhattan(i, j-1, dest)
				fNew = gNew + hNew 

				if cellInfo[i][j-1].f == MAX or cellInfo[i][j-1].f > fNew:
					openList.append(OpenListElement(fNew, Pair(i, j-1)))
					cellInfo[i][j-1].f = fNew 
					cellInfo[i][j-1].g = gNew
					cellInfo[i][j-1].h = hNew  
					cellInfo[i][j-1].parent_x = i 
					cellInfo[i][j-1].parent_y = j
		 
		
	if foundDest == False:
		print('Failed to find the destination cell\n')
	
	return None 

if __name__ == "__main__":
	# 0 means there's a wall
	print('Enter : 0 for Euclidian heuristic \n \t 1 for Diagonal heuristic \n \t 2 for Manhattan Heuristic\n')
	heuristic_option = input()
	print('\n')
	grid = ([
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 0, 0, 0, 0, 1, 1, 1],
		[1, 0, 1, 1, 0, 1, 0, 1],
		[1, 0, 1, 1, 0, 1, 0, 1],
		[1, 0, 1, 1, 0, 1, 0, 1],
		[1, 0, 1, 1, 1, 1, 0, 1],
		[1, 0, 0, 0, 0, 0, 0, 1],
		[1, 1, 1, 1, 1, 1, 1, 1]
	])

	src = Pair(3,2)
	dest = Pair(3, 7)
	path = []
	path = aStarSearch(grid, src, dest)
	draw_map(grid, (src.x,src.y), (dest.x,dest.y), path)

	


	
