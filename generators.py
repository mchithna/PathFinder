# handles how we build the mazes

import random

def remove_walls(current, next_cell):
    # find out where the next cell is relative to current cell
    dx = current.x - next_cell.x 
    dy = current.y - next_cell.y

    # when dx = -1 , next is to the RIGHT 
    if dx == -1:
        current.walls[1] = False
        next_cell.walls[3] = False 
    # when dx = 1 , next is to the LEFT 
    if dx == 1:
        current.walls[3] = False
        next_cell.walls[1] = False

    # when dy = -1 , next is to the BELOW
    if dy == -1:
        current.walls[2] = False
        next_cell.walls[0] = False
    # when dy = 1 , next is to the ABOVE
    if dy == 1:
        current.walls[0] = False
        next_cell.walls[2] = False


# -- Recursive Backtracker algorithm class
class DFSGenerator:
    def __init__(self, start_cell, cols, rows):
        self.current_cell = start_cell
        self.current_cell.visited = True
        self.stack = []
        self.cols = cols
        self.rows = rows

    def step(self, grid_cells):
        # check neighbors 
        next_cell = self.current_cell.check_neighbors(grid_cells)
        
        if next_cell:
            # if neighbor found
            next_cell.visited = True
            self.stack.append(self.current_cell) # save the position
            remove_walls(self.current_cell, next_cell) # break wall
            self.current_cell = next_cell # move there
            return self.current_cell
        
        elif len(self.stack) > 0:
            # if stuck , backtrack
            self.current_cell = self.stack.pop()
            return self.current_cell
        
        else:
            # if finished (empty stack)
            return None
        

# -- Prim's Algorithm Class
class PrimGenerator:
    def __init__(self, start_cell, cols, rows):
        self.cols = cols
        self.rows = rows
        self.frontier = []
        self.current_cell = start_cell
        self.current_cell.visited = True
        self.is_started = False

    def get_neighbors(self, cell, grid_cells, visited_status):
        # Helper function to find neighbors based on whether they are in the maze yet
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Top, Right, Bottom, Left
        
        for dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                idx = nx + ny * self.cols
                neighbor = grid_cells[idx]
                if neighbor.visited == visited_status:
                    neighbors.append(neighbor)
        return neighbors

    def step(self, grid_cells):
        # 1. On the very first step, add the start cell's neighbors to the frontier
        if not self.is_started:
            unvisited_neighbors = self.get_neighbors(self.current_cell, grid_cells, False)
            for n in unvisited_neighbors:
                if n not in self.frontier:
                    self.frontier.append(n)
            self.is_started = True
            return self.current_cell

        # 2. If the frontier is empty, the maze is done
        if not self.frontier:
            return None 

        # 3. Pick a random cell from the frontier
        next_cell = random.choice(self.frontier)
        self.frontier.remove(next_cell)

        # 4. Find its neighbors that are ALREADY in the maze
        visited_neighbors = self.get_neighbors(next_cell, grid_cells, True)
        
        if visited_neighbors:
            # 5. Pick a random visited neighbor and carve a path between them
            in_maze_neighbor = random.choice(visited_neighbors)
            remove_walls(next_cell, in_maze_neighbor)

        # 6. Mark the new cell as part of the maze
        next_cell.visited = True
        self.current_cell = next_cell

        # 7. Add the new cell's unvisited neighbors to the frontier
        unvisited_neighbors = self.get_neighbors(next_cell, grid_cells, False)
        for n in unvisited_neighbors:
            if n not in self.frontier:
                self.frontier.append(n)

        return self.current_cell