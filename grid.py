import pygame
from settings import * 

import random

class Cell:
    def __init__ (self, x, y, tile_size, cols, rows):
        self.x = x
        self.y = y
        self.tile_size = tile_size # Dynamic now!
        self.cols = cols
        self.rows = rows

        # keeps track of the 4 walls in a cell (top, right, bottom, left)
        self.walls = [True, True, True, True]
        self.visited = False

        # identify the start and end 
        self.is_start = False
        self.is_end = False
        # identify the path
        self.is_scanned = False
        self.is_path = False

    def draw(self, screen):
        x =  self.x * self.tile_size
        y = self.y * self.tile_size

        # tile colouring
        if self.is_start:
            pygame.draw.rect(screen, START_COLOUR, (x, y, self.tile_size, self.tile_size))
        elif self.is_end:
            pygame.draw.rect(screen, END_COLOUR, (x, y, self.tile_size, self.tile_size))
        elif self.is_path:
            pygame.draw.rect(screen, PATH_COLOUR, (x, y, self.tile_size, self.tile_size))
        elif self.is_scanned:
            pygame.draw.rect(screen, SCAN_COLOUR, (x, y, self.tile_size, self.tile_size))
        elif self.visited:
            pygame.draw.rect(screen, VISITED_COLOUR, (x, y, self.tile_size, self.tile_size))

        # check if the wall is true, then draw line 

        # top wall
        if self.walls[0]:
            pygame.draw.line(screen, GRID_COLOUR, (x, y), (x + self.tile_size, y), 1)
        # right wall 
        if self.walls[1]:
            pygame.draw.line(screen, GRID_COLOUR, (x + self.tile_size, y),(x + self.tile_size, y + self.tile_size), 1)        
        # bottom wall 
        if self.walls[2]:
            pygame.draw.line(screen, GRID_COLOUR, (x + self.tile_size, y + self.tile_size), (x, y + self.tile_size), 1)        
        # left wall
        if self.walls[3]:
            pygame.draw.line(screen, GRID_COLOUR, (x, y + self.tile_size), (x, y), 1)
        
    # check the availability of neighbor cells and return random cell
    def check_neighbors(self, grid_cells):
        neighbors = []

        # helper function - find a cell in the list 
        def get_index(x,y):
            if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
                return -1 #out of bounds
            return x + (y * self.cols) 

        # get indexes of the 4 neighbor cells 
        top_index = get_index(self.x, self.y -1)
        right_index = get_index(self.x +1, self.y)
        bottom_index = get_index(self.x, self.y +1)
        left_index = get_index(self.x -1, self.y )

        # check if the cells are valid and NOT already visited
        if top_index != -1 and not grid_cells[top_index].visited:
            neighbors.append(grid_cells[top_index])
        if right_index != -1 and not grid_cells[right_index].visited:
            neighbors.append(grid_cells[right_index])
        if bottom_index != -1 and not grid_cells[bottom_index].visited:
            neighbors.append(grid_cells[bottom_index])
        if left_index != -1 and not grid_cells[left_index].visited:
            neighbors.append(grid_cells[left_index])

        # returns a random cell index or none
        if neighbors:
            return random.choice(neighbors)
        else:
            return None
        

def init_grid(tile_size):
    # calculate columns and rows with tile size
    cols = MAZE_WIDTH // tile_size
    rows = MAZE_HEIGHT // tile_size
    
    cells = []
    for row in range(rows):
        for col in range(cols):
            cell = Cell(col, row, tile_size, cols, rows)
            cells.append(cell)
    return cells, cols, rows 