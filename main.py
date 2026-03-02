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

    # Size Configurations
    sizes = {"S": 80, "M": 40, "L": 20, "XL": 10} # Values are tile size
    current_size = "M"
    tile_size = sizes[current_size]
    
    # create grid
    grid_cells, cols, rows = init_grid(tile_size)

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

    btn_s = Button(850, 200, 50, 40, "S")
    btn_m = Button(915, 200, 50, 40, "M")
    btn_l = Button(980, 200, 50, 40, "L")
    btn_xl = Button(1045, 200, 50, 40, "XL")

    # speed configurations 
    speeds = {"x0.1": 0.1, "x0.5": 0.5, "x1": 1, "x5": 5, "x10": 10}
    current_speed = "x1"
    step_accumulator = 0.0

    btn_spd_01 = Button(850, 290, 45, 40, ".1x")
    btn_spd_05 = Button(901, 290, 45, 40, ".5x")
    btn_spd_1  = Button(952, 290, 45, 40, "1x")
    btn_spd_5  = Button(1003, 290, 45, 40, "5x")
    btn_spd_10 = Button(1054, 290, 45, 40, "10x")

    # Algorithm configurations
    current_generator = "DFS"
    btn_gen_dfs = Button(850, 380, 80, 40, "DFS")
    btn_gen_prim = Button(940, 380, 80, 40, "Prim")

    current_solver = "BFS"
    btn_sol_bfs = Button(850, 470, 70, 40, "BFS")
    btn_sol_dfs = Button(930, 470, 70, 40, "DFS")
    btn_sol_astar = Button(1010, 470, 70, 40, "A*")

    ui_font = pygame.font.SysFont('Arial', 20)

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if btn_spd_01.is_clicked(event): current_speed = "x0.1"
            if btn_spd_05.is_clicked(event): current_speed = "x0.5"
            if btn_spd_1.is_clicked(event): current_speed = "x1"
            if btn_spd_5.is_clicked(event): current_speed = "x5"
            if btn_spd_10.is_clicked(event): current_speed = "x10"

            # algorithm selectors logic 
            if btn_gen_dfs.is_clicked(event): current_generator = "DFS"
            if btn_gen_prim.is_clicked(event): current_generator = "Prim"
            
            if btn_sol_bfs.is_clicked(event): current_solver = "BFS"
            if btn_sol_dfs.is_clicked(event): current_solver = "DFS"
            if btn_sol_astar.is_clicked(event): current_solver = "A*"
            
            #  size Buttons logic 
            new_size = None
            if btn_s.is_clicked(event): new_size = "S"
            if btn_m.is_clicked(event): new_size = "M"
            if btn_l.is_clicked(event): new_size = "L"
            if btn_xl.is_clicked(event): new_size = "XL"

            if new_size and new_size != current_size:
                current_size = new_size
                tile_size = sizes[current_size]
                grid_cells, cols, rows = init_grid(tile_size)

                start_cell = grid_cells[0]
                end_cell = grid_cells[-1]
                start_cell.is_start = True
                end_cell.is_end = True
                
                current_cell = start_cell
                current_cell.visited = True
                stack = []
                bfs_queue = deque()
                bfs_visited = set()
                parent_map = {}
                is_generating = False
                is_solving = False

            # generate button event
            if btn_generate.is_clicked(event):
                # reset grid for a new maze
                grid_cells, cols, rows = init_grid(tile_size)
                start_cell = grid_cells[0]
                end_cell = grid_cells[-1]
                start_cell.is_start = True
                end_cell.is_end = True

                # reset the configurations
                current_cell = start_cell
                current_cell.visited = True
                stack = []
                bfs_queue = deque()
                bfs_visited = set()
                parent_map = {}
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
        
        # Game logic

        steps_this_frame = 0
        if is_generating or is_solving:
            step_accumulator += speeds[current_speed]
            steps_this_frame = int(step_accumulator)
            step_accumulator -= steps_this_frame


        # 1. maze generator logic
        if is_generating:
            # recursive calling 
            for _ in range(steps_this_frame): ## NOT PERMENANT ONLY FOR TESTING
                if current_generator == "DFS":
                    new_cell = recursive_backtracker(current_cell, grid_cells, stack)
                elif current_generator == "Prim":
                    # placeholder for Prim algo 
                    new_cell = recursive_backtracker(current_cell, grid_cells, stack)

                if new_cell:
                    current_cell = new_cell
                else:
                    is_generating = False 
                    print("Maze Generation Complete.")
                    break
        
        # 2. maze solver logic
        if is_solving:
            for _ in range(steps_this_frame):
                if current_solver == "BFS":
                    current_processed = step_bfs(bfs_queue, bfs_visited, parent_map, grid_cells, cols, rows)
                elif current_solver in ["DFS", "A*"]:
                    # placeholder for DFS and A* algo
                    current_processed = step_bfs(bfs_queue, bfs_visited, parent_map, grid_cells, cols, rows)

                if current_processed is None:  # queue is empty 
                    is_solving = False
                    print("No Path Possible.")
                    break
                elif current_processed == end_cell:  # end cell found
                    is_solving = False
                    print("Path Found!")

                    temp = end_cell
                    while temp is not None:
                        temp.is_path = True
                        temp = parent_map.get(temp)
                    break

        # visuals
        screen.fill(GREY)
        # draw grid
        for cell in grid_cells:
            cell.draw(screen)
        
        # highlight the Head
        if is_generating:
            x = current_cell.x * tile_size
            y = current_cell.y * tile_size
            pygame.draw.rect(screen, (20, 240, 20), (x, y, tile_size, tile_size))

        # draw the controls n sidebar
        draw_sidebar(screen)
        btn_generate.draw(screen)
        btn_solve.draw(screen)

        # draw size ui elements
        size_label = ui_font.render("Maze Size", True, TEXT_COLOUR)
        screen.blit(size_label, (850, 175))
        
        btn_s.draw(screen, is_active=(current_size == "S"))
        btn_m.draw(screen, is_active=(current_size == "M"))
        btn_l.draw(screen, is_active=(current_size == "L"))
        btn_xl.draw(screen, is_active=(current_size == "XL"))

        # draw speed ui elements
        speed_label = ui_font.render("Animation Speed", True, TEXT_COLOUR)
        screen.blit(speed_label, (850, 260))

        btn_spd_01.draw(screen, is_active=(current_speed == "x0.1"))
        btn_spd_05.draw(screen, is_active=(current_speed == "x0.5"))
        btn_spd_1.draw(screen, is_active=(current_speed == "x1"))
        btn_spd_5.draw(screen, is_active=(current_speed == "x5"))
        btn_spd_10.draw(screen, is_active=(current_speed == "x10"))

        # draw algo ui elements
        gen_label = ui_font.render("Generator Algorithm", True, TEXT_COLOUR)
        screen.blit(gen_label, (850, 350))
        btn_gen_dfs.draw(screen, is_active=(current_generator == "DFS"))
        btn_gen_prim.draw(screen, is_active=(current_generator == "Prim"))

        sol_label = ui_font.render("Solver Algorithm", True, TEXT_COLOUR)
        screen.blit(sol_label, (850, 440))
        btn_sol_bfs.draw(screen, is_active=(current_solver == "BFS"))
        btn_sol_dfs.draw(screen, is_active=(current_solver == "DFS"))
        btn_sol_astar.draw(screen, is_active=(current_solver == "A*"))

        pygame.display.flip() 
        clock.tick(FPS) # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()