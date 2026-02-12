# handles how we build the mazes

def remove_walls(current, next):
    # find out where the next cell is relative to current cell
    dx = current.x - next.x 
    dy = current.y - next.y

    # when dx = -1 , next is to the RIGHT 
    if dx == -1:
        current.walls[1] = False
        next.walls[3] = False 
    # when dx = 1 , next is to the LEFT 
    if dx == 1:
        current.walls[3] = False
        next.walls[1] = False

    # when dy = -1 , next is to the BELOW
    if dy == -1:
        current.walls[2] = False
        next.walls[0] = False
    # when dy = 1 , next is to the ABOVE
    if dy == 1:
        current.walls[0] = False
        next.walls[2] = False

# -- Recursive Backtracker algorithm

def recursive_backtracker(current_cell, grid_cells, stack):

    # check neighbors 
    next_cell = current_cell.check_neighbors(grid_cells)
    
    if next_cell:
        # if neighbor found
        next_cell.visited = True
        stack.append(current_cell) # save the position
        remove_walls(current_cell, next_cell) # break wall
        return next_cell # move there
    
    elif len(stack) > 0:
        # if stuck , backtrack
        return stack.pop()
    
    else:
        # if finished (empty stack)
        return None