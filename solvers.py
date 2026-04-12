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
    
# -- Wall Follower (Right-Hand) Algorithm Class
class WallFollowerSolver:
    def __init__(self, start_cell, end_cell, cols, rows):
        self.current_cell = start_cell
        self.end_cell = end_cell
        self.cols = cols
        self.rows = rows
        
        self.visited = {start_cell}
        
        # heading - 0=top, 1=right, 2=bottom, 3=left
        # start by looking for the first open wall so we know which way to face
        self.heading = 0
        for i in range(4):
            if not start_cell.walls[i]:
                self.heading = i
                break
                
        self.path_stack = [start_cell]
        self.parent_map = {start_cell: None}

    def get_index(self, x, y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows: 
            return -1 
        return x + (y * self.cols)

    def step(self, grid_cells):
        if self.current_cell == self.end_cell:
            return self.current_cell # Done!
        
        self.current_cell.is_scanned = True
        
        # 0:top (y-1), 1:right (x+1), 2:bottom (y+1), 3:left (x-1)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        # right-hand rule priority: Right, Straight, Left, Backwards
        right_dir = (self.heading + 1) % 4
        straight_dir = self.heading
        left_dir = (self.heading - 1) % 4
        back_dir = (self.heading + 2) % 4
        
        check_order = [right_dir, straight_dir, left_dir, back_dir]
        
        next_cell = None
        for move_dir in check_order:
            if not self.current_cell.walls[move_dir]:
                dx, dy = moves[move_dir]
                idx = self.get_index(self.current_cell.x + dx, self.current_cell.y + dy)
                if idx != -1:
                    next_cell = grid_cells[idx]
                    self.heading = move_dir # turn to face the new direction!
                    break
                    
        if next_cell:
            self.visited.add(next_cell)
            
            # path tracking (to dynamically build the parent_map for main.py)
            if len(self.path_stack) > 1 and next_cell == self.path_stack[-2]:
                # backtracking... remove the dead end from our final yellow path
                popped_cell = self.path_stack.pop()
                if popped_cell in self.parent_map:
                    del self.parent_map[popped_cell]
            else:
                # moving forward... add to our final yellow path
                self.parent_map[next_cell] = self.current_cell
                self.path_stack.append(next_cell)
                
            self.current_cell = next_cell
            return self.current_cell
            
        return None # stuck (justin case)

    
# -- Dead-End Filling Algorithm Class
class DeadEndSolver:
    def __init__(self, start_cell, end_cell, cols, rows):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.cols = cols
        self.rows = rows
        
        self.dead_ends = deque()
        self.visited = set() # set for scanned cell counter 
        self.parent_map = {}
        self.exit_counts = {}
        
        self.initialized = False
        self.finished = False

    def get_index(self, x, y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows: return -1
        return x + (y * self.cols)
        
    def get_open_neighbors(self, cell, grid_cells):
        # returns neighbors that are NOT blocked by a wall
        neighbors = []
        directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)] # Top, Right, Bottom, Left
        for dx, dy, wall_idx in directions:
            if not cell.walls[wall_idx]:
                idx = self.get_index(cell.x + dx, cell.y + dy)
                if idx != -1:
                    neighbors.append(grid_cells[idx])
        return neighbors

    def init_dead_ends(self, grid_cells):
        # scan the whole grid once to find all initial dead ends
        for cell in grid_cells:
            neighbors = self.get_open_neighbors(cell, grid_cells)
            self.exit_counts[cell] = len(neighbors)
            # dead end has exactly 1 open exit (and is NOT the start or end cell)
            if len(neighbors) == 1 and cell != self.start_cell and cell != self.end_cell:
                self.dead_ends.append(cell)
        self.initialized = True

    def build_parent_map(self, grid_cells):
        # once all dead ends are filled, only the correct path remains...
        # we do a quick invisible BFS on the remaining empty cells so main.py can draw the yellow path
        queue = deque([self.start_cell])
        temp_visited = {self.start_cell}
        
        while queue:
            curr = queue.popleft()
            if curr == self.end_cell:
                break
            for n in self.get_open_neighbors(curr, grid_cells):
                if n not in self.visited and n not in temp_visited:
                    temp_visited.add(n)
                    self.parent_map[n] = curr
                    queue.append(n)

    def step(self, grid_cells):
        if not self.initialized:
            self.init_dead_ends(grid_cells)

        # if there are no more dead ends to fill...
        if not self.dead_ends:
            if not self.finished:
                self.finished = True
                self.build_parent_map(grid_cells)
                # trick main.py into thinking we "found" the end cell so it draws the yellow line
                return self.end_cell 
            return None
        
        # pop a dead end and fill it
        curr = self.dead_ends.popleft()
        self.visited.add(curr)
        curr.is_scanned = True # Turn the dead end blue

        # find its open neighbor and reduce its exit count by 1
        neighbors = self.get_open_neighbors(curr, grid_cells)
        for n in neighbors:
            if n not in self.visited:
                self.exit_counts[n] -= 1
                # if the neighbor now only has 1 exit left, it has become a new dead end!
                if self.exit_counts[n] == 1 and n != self.start_cell and n != self.end_cell:
                    self.dead_ends.append(n)
        
        return curr