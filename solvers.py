# handles how we solve the mazes

from collections import deque
from settings import *
import heapq

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

# -- A* search algorithm class
class AStarSolver:
    def __init__(self, start_cell, end_cell, cols, rows):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.cols = cols
        self.rows = rows
        
        # tie-breaker for the priority queue 
        self.count = 0 
        
        # priority queue for storing tuples of (f_score, count, cell)
        self.open_set = []
        heapq.heappush(self.open_set, (0, self.count, start_cell))
        
        self.g_score = {start_cell: 0}
        self.f_score = {start_cell: self.heuristic(start_cell, end_cell)}
        
        # to quickly check if a cell is in the open_set
        self.open_set_hash = {start_cell} 
        
        self.visited = set()
        self.parent_map = {start_cell: None}

    def heuristic(self, cell1, cell2):
        # Manhattan Distance formula
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    def get_index(self, x, y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows: 
            return -1 
        return x + (y * self.cols)

    def step(self, grid_cells):
        if not self.open_set:
            return None # path is finished (or blocked)
        
        # pop the cell with the LOWEST f_score (the best guess)
        current_cell = heapq.heappop(self.open_set)[2]
        self.open_set_hash.remove(current_cell)
        
        self.visited.add(current_cell)
        current_cell.is_scanned = True
        
        if current_cell == self.end_cell:
            return current_cell # found it!
            
        # directions: Top (0,-1), Right (1,0), Bottom (0,1), Left (-1,0)
        directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
        
        for dx, dy, wall_idx in directions:
            if not current_cell.walls[wall_idx]: 
                idx = self.get_index(current_cell.x + dx, current_cell.y + dy)
                if idx != -1:
                    neighbor = grid_cells[idx]
                    
                    if neighbor in self.visited:
                        continue
                        
                    # the distance from start to this neighbor is current distance + 1
                    temp_g_score = self.g_score[current_cell] + 1
                    
                    # if we found a faster way to this neighbor (or first time seeing it)
                    if neighbor not in self.g_score or temp_g_score < self.g_score[neighbor]:
                        self.parent_map[neighbor] = current_cell
                        self.g_score[neighbor] = temp_g_score
                        self.f_score[neighbor] = temp_g_score + self.heuristic(neighbor, self.end_cell)
                        
                        if neighbor not in self.open_set_hash:
                            self.count += 1
                            heapq.heappush(self.open_set, (self.f_score[neighbor], self.count, neighbor))
                            self.open_set_hash.add(neighbor)

        return current_cell