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
    