import pygame
import sys
from settings import *
from grid import init_grid
from generators import remove_walls 
from generators import recursive_backtracker 

def main():
    # window setup 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CS50 Pathfinder")
    clock = pygame.time.Clock()

    # create grid
    grid_cells = init_grid()
    
    # generator configurations
    current_cell = grid_cells[0]
    current_cell.visited = True
    stack = [] # backtracking path

    # indicator
    is_generating = True 


    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        # maze logic
        if is_generating:
            # recursive calling 
            new_cell = recursive_backtracker(current_cell, grid_cells, stack)
            
            if new_cell:
                current_cell = new_cell
            else:
                is_generating = False # stop
                print("Maze Generation Complete.")

        # visuals
        screen.fill(GREY)
        # draw grid
        for cell in grid_cells:
            cell.draw(screen)
        
        # highlight the Head
        if is_generating:
            x = current_cell.x * TILE_SIZE
            y = current_cell.y * TILE_SIZE
            pygame.draw.rect(screen, (20, 240, 20), (x, y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip() 

        clock.tick(FPS) # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()