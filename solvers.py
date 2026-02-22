# handles how we solve the mazes

from settings import *

# -- Breadth-First Search algorithm
def step_bfs(queue, visited, parent_map, grid_cells, cols, rows):
    if not queue:
        return None # path is finished
    
    # pop the next cell to check
    current_cell = queue.popleft()
    current_cell.is_scanned = True

    # helper function to find the neighor cell index
    def get_index(x, y):
        if x < 0 or x >= cols or y < 0 or y >= rows: 
            return -1 # no neighbors
        return x + (y * cols)
    
    # check all directions for walls

    # top 
    if not current_cell.walls[0]: 
        idx = get_index(current_cell.x, current_cell.y - 1)
        if idx != -1:
            neighbor = grid_cells[idx]
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_cell # Remember who found me
                queue.append(neighbor)
    
    # right 
    if not current_cell.walls[1]: 
        idx = get_index(current_cell.x + 1, current_cell.y)
        if idx != -1:
            neighbor = grid_cells[idx]
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_cell
                queue.append(neighbor)
    
    # bottom
    if not current_cell.walls[2]: 
        idx = get_index(current_cell.x, current_cell.y + 1)
        if idx != -1:
            neighbor = grid_cells[idx]
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_cell
                queue.append(neighbor)
    
    # left 
    if not current_cell.walls[3]: 
        idx = get_index(current_cell.x - 1, current_cell.y)
        if idx != -1:
            neighbor = grid_cells[idx]
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_cell
                queue.append(neighbor)

    return current_cell
