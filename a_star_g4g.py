import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


# plot map and path
def draw_map(grid, start_node, goal_node, path=None):
    fig, ax = plt.subplots(figsize=(12,12))
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

def generate_successor(grid, node):
    successors = []
    x = node[0]
    y = node[1]
    if x == 0 and y == 0:
        if grid[x+1][y+1] != 0:
            successors.append((x+1, y+1))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
        if grid[x][y+1] != 0:
            successors.append((x, y+1))
    elif x == len(grid)-1 and y == len(grid[0])-1:
        if grid[x-1][y-1] != 0:
            successors.append((x-1, y-1))
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x-1][y] != 0:
            successors.append((x-1, y))
    elif x == 0 and y == len(grid[0])-1:
        if grid[x+1][y-1] != 0:
            successors.append((x+1, y-1))
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
    elif x == len(grid)-1 and y == 0:
        if grid[x+1][y-1] != 0:
            successors.append((x+1, y-1))
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
    elif x == 0 and y > 0 and y < len(grid[0]) - 1:
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x][y+1] != 0:
            successors.append((x, y+1))
        if grid[x+1][y-1] != 0:
            successors.append((x+1, y-1))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
        if grid[x+1][y+1] != 0:
            successors.append((x+1, y+1))
    elif x == len(grid)-1 and y > 0 and y < len(grid[0]) - 1:
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x][y+1] != 0:
            successors.append((x, y+1))
        if grid[x-1][y-1] != 0:
            successors.append((x-1, y-1))
        if grid[x-1][y] != 0:
            successors.append((x-1, y))
        if grid[x-1][y+1] != 0:
            successors.append((x-1, y+1))
    elif y == 0 and x > 0 and x < len(grid) - 1:
        if grid[x][y+1] != 0:
            successors.append((x, y+1))
        if grid[x-1][y] != 0:
            successors.append((x-1, y))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
        if grid[x+1][y+1] != 0:
            successors.append((x+1, y+1))
        if grid[x-1][y+1] != 0:
            successors.append((x-1, y+1))
    elif y == len(grid[0])-1 and x > 0 and x < len(grid) - 1:
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x-1][y] != 0:
            successors.append((x-1, y))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
        if grid[x-1][y-1] != 0:
            successors.append((x-1, y-1))
        if grid[x+1][y-1] != 0:
            successors.append((x+1, y-1))
    else:
        if grid[x-1][y-1] != 0:
            successors.append((x-1, y-1))
        if grid[x-1][y] != 0:
            successors.append((x-1, y))
        if grid[x-1][y+1] != 0:
            successors.append((x-1, y+1))
        if grid[x][y-1] != 0:
            successors.append((x, y-1))
        if grid[x][y+1] != 0:
            successors.append((x, y+1))
        if grid[x+1][y-1] != 0:
            successors.append((x+1, y-1))
        if grid[x+1][y] != 0:
            successors.append((x+1, y))
        if grid[x+1][y+1] != 0:
            successors.append((x+1, y+1))

    return successors
def heuristic_manhattan(node, goal_node):
    return (abs(node[0]-goal_node[0]) + abs(node[1]-goal_node[1]))
def heuristic_diagonal(node, goal_node):
    return max(abs(node[0]-goal_node[0]), abs(node[1]-goal_node[1]))
def least_f(f, open_list):
    min = 10000
    q = ()
    if len(open_list) == 0:
        print("list empty")
        return None 
    for x in open_list:
        if x in f:
            if f[x] < min:
                min = f[x]
                q = x 
        else:
            continue
    
    return q
    
def a_star(grid, start_node, goal_node):
    f = {}
    g = {}
    parents = {}
    open_list = []
    closed_list = []
    open_list.append(start_node)
    g[start_node] = 0
    f[start_node] = heuristic_diagonal(start_node, goal_node) + g[start_node]

    while open_list:
        q = least_f(f, open_list)
        open_list.remove(q)
        successors = generate_successor(grid, q)
        parents[q] = successors

        for successor in successors:
            if successor == goal_node:
                
                g[successor] = g[q] + 1
                f[successor] = heuristic_diagonal(successor, goal_node) + g[successor]
                
                closed_list.append(q)
                closed_list.append(successor)
                
                return closed_list
            
                
            if successor in open_list:
                for x in open_list:
                    if x == successor and f[x] < f[successor]:
                        continue
            
                
            if successor in closed_list:
                for x in closed_list:
                    if x == successor and f[x] < f[successor]:
                        continue
                    
            f[successor] = heuristic_diagonal(successor, goal_node)
            g[successor] = g[q] + heuristic_diagonal(q, successor)
            open_list.append(successor)
        closed_list.append(q)
    
        

if __name__ == "__main__":
    
    grid = ([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1]
    ])

    start_node = (0, 0)
    goal_node = (3, 7)
    path = []
    
    draw_map(grid, start_node, goal_node)

    if grid[goal_node[0]][goal_node[1]] != 0:
        path = a_star(grid, start_node, goal_node)
        draw_map(grid, start_node, goal_node, path)
        print(path)
    else:
        print("Goal position in wall")
        pass 
    


