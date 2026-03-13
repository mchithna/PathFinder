# handles how we solve the mazes

from collections import deque
from settings import *

# -- BFS algorithm class
class BFSSolver:
    def __init__(self, start_cell, end_cell, cols, rows):
        self.queue = deque([start_cell])
        self.visited = {start_cell}
        self.parent_map = {start_cell: None}
        self.end_cell = end_cell
        self.cols = cols
        self.rows = rows

    def get_index(self, x, y):
        # helper function to find the neighor cell index
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows: 
            return -1 # no neighbors
        return x + (y * self.cols)

    def step(self, grid_cells):
        if not self.queue:
            return None # path is finished (or no path possible)
        
        # pop the next cell to check
        current_cell = self.queue.popleft()
        current_cell.is_scanned = True
        
        # check all directions for walls

        # top 
        if not current_cell.walls[0]: 
            idx = self.get_index(current_cell.x, current_cell.y - 1)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell # Remember who found me
                    self.queue.append(neighbor)
        
        # right 
        if not current_cell.walls[1]: 
            idx = self.get_index(current_cell.x + 1, current_cell.y)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.queue.append(neighbor)
        
        # bottom
        if not current_cell.walls[2]: 
            idx = self.get_index(current_cell.x, current_cell.y + 1)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.queue.append(neighbor)
        
        # left 
        if not current_cell.walls[3]: 
            idx = self.get_index(current_cell.x - 1, current_cell.y)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.queue.append(neighbor)

        return current_cell

# -- DFS algorithm class
class DFSSolver:
    def __init__(self, start_cell, end_cell, cols, rows):
        self.stack = [start_cell]
        self.visited = {start_cell}
        self.parent_map = {start_cell: None}
        self.end_cell = end_cell
        self.cols = cols
        self.rows = rows

    def get_index(self, x, y):
        # helper function to find the neighor cell index
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows: 
            return -1 
        return x + (y * self.cols)

    def step(self, grid_cells):
        if not self.stack:
            return None # path is finished (or no path possible)
        
        # pop the LAST cell added 
        current_cell = self.stack.pop()
        current_cell.is_scanned = True
        
        # check all directions for walls
        
        # top 
        if not current_cell.walls[0]: 
            idx = self.get_index(current_cell.x, current_cell.y - 1)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.stack.append(neighbor)
        
        # right 
        if not current_cell.walls[1]: 
            idx = self.get_index(current_cell.x + 1, current_cell.y)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.stack.append(neighbor)
        
        # bottom
        if not current_cell.walls[2]: 
            idx = self.get_index(current_cell.x, current_cell.y + 1)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.stack.append(neighbor)
        
        # left 
        if not current_cell.walls[3]: 
            idx = self.get_index(current_cell.x - 1, current_cell.y)
            if idx != -1:
                neighbor = grid_cells[idx]
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent_map[neighbor] = current_cell
                    self.stack.append(neighbor)

        return current_cell