# handles how we build the mazes


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

