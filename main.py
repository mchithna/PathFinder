import pygame
import sys
from settings import *
from grid import init_grid
from generators import recursive_backtracker 
from solvers import step_bfs
from ui import Button, draw_sidebar
from collections import deque


def main():
    # window setup 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CS50 Pathfinder")
    clock = pygame.time.Clock()

    # create grid
    grid_cells = init_grid()

    # define start and end 
    start_cell = grid_cells[0]
    end_cell = grid_cells[-1]

    start_cell.is_start = True
    end_cell.is_end = True
    
    # generator configurations
    current_cell = grid_cells[0]
    current_cell.visited = True
    stack = [] # backtracking path

    # solver configurations
    bfs_queue = deque()
    bfs_visited = set()
    parent_map = {} # to construct the path

    # state indicator
    is_generating = False
    is_solving = False

    # UI setup
    btn_generate = Button(MAZE_WIDTH + 25, 50, 150, 50, "Generate")
    btn_solve = Button(MAZE_WIDTH + 25, 120, 150, 50, "Solve")

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            # generate button event
            if btn_generate.is_clicked(event):
                # reset grid for a new maze
                grid_cells = init_grid()
                start_cell = grid_cells[0]
                end_cell = grid_cells[-1]
                start_cell.is_start = True
                end_cell.is_end = True

                # reset the configurations
                current_cell = start_cell
                current_cell.visited = True
                stack = []
                is_generating = True
                is_solving = False
            
            if btn_solve.is_clicked(event):
                if not is_generating: # solve when maze is ready
                    # reset cell states
                    for cell in grid_cells:
                        cell.is_scanned = False
                        cell.is_path = False
                        
                    bfs_queue = deque([start_cell])
                    bfs_visited = {start_cell}
                    parent_map = {start_cell: None}
                    is_solving = True


        # 1. maze generator logic
        if is_generating:
            # recursive calling 
            new_cell = recursive_backtracker(current_cell, grid_cells, stack)
            
            if new_cell:
                current_cell = new_cell
            else:
                is_generating = False # stop
                print("Maze Generation Complete.")
        
        # 2. maze solver logic
        if is_solving:
            current_processed = step_bfs(bfs_queue, bfs_visited, parent_map, grid_cells)

            if current_processed is None:  # queue is empty 
                is_solving = False
                print("No Path Possible.")
            elif current_processed == end_cell:  # end cell found
                is_solving = False
                print("Path Found!")

                temp = end_cell
                while temp is not None:
                    temp.is_path = True
                    temp = parent_map.get(temp)

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

        # draw the controls n sidebar
        draw_sidebar(screen)
        btn_generate.draw(screen)
        btn_solve.draw(screen)

        pygame.display.flip() 
        clock.tick(FPS) # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()