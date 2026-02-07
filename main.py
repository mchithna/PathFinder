import pygame
import sys
from settings import *
from grid import init_grid
from generators import remove_walls

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

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        # -- Backtracking algo -- 
        # check for neighbors
        next_cell = current_cell.check_neighbors(grid_cells)

        if next_cell:
            next_cell.visited = True

            # add current cell into stack
            stack.append(current_cell)

            # remove the walls 
            remove_walls(current_cell, next_cell)

            # proceed to next
            current_cell = next_cell

        elif len(stack) > 0:
            # if stuck , backtrack
            current_cell = stack.pop()


        # visuals
        screen.fill(GREY)
        # draw grid
        for cell in grid_cells:
            cell.draw(screen)
        
        # highlight the Head
        x = current_cell.x * TILE_SIZE
        y = current_cell.y * TILE_SIZE
        pygame.draw.rect(screen, (20, 240, 20), (x, y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip() 

        clock.tick(FPS) # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()