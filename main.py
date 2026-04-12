import pygame
import asyncio 
from settings import *
from collections import deque
from grid import init_grid
from generators import *
from solvers import *
from ui import Button, draw_sidebar, draw_status_bar, SteppedSlider


async def main():  # .make the main function asynchronous
    # window setup 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CS50 Pathfinder")
    clock = pygame.time.Clock()

    # size configurations
    sizes = {"S": 50, "M": 25, "L": 20, "XL": 10} # values are tile size
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
    current_solver_head = None

    # analytics variables
    scanned_count = 0
    path_count = 0
    efficiency = 0
    start_time = 0
    final_status_text = "Idle"

    # The strategy objects
    active_generator = DFSGenerator(start_cell, cols, rows)
    active_solver = None

    # UI and font setup
    ui_font = pygame.font.SysFont(['poppins', 'segoe ui', 'helvetica', 'arial'], 18)
    title_font = pygame.font.SysFont(['poppins', 'segoe ui', 'helvetica', 'arial'], 36, bold=True)
    
    # action buttons
    btn_generate = Button(830, 505, 160, 50, "Generate", style="primary")
    btn_solve = Button(1010, 505, 160, 50, "Solve", style="secondary")


    # maze size buttons
    btn_s = Button(830, 100, 50, 46, "S", "8x6")
    btn_m = Button(890, 100, 50, 46, "M", "20x15")
    btn_l = Button(950, 100, 50, 46, "L", "40x30")
    btn_xl = Button(1010, 100, 50, 46, "XL", "80x60")

    # generator algorithms
    current_generator = "DFS"
    btn_gen_dfs = Button(830, 190, 160, 40, "DFS")
    btn_gen_prim = Button(1010, 190, 160, 40, "Prim")
    btn_gen_kruskal = Button(830, 240, 160, 40, "Kruskal")
    btn_gen_wilson = Button(1010, 240, 160, 40, "Wilson")

    # solver algorithms
    current_solver = "BFS"
    btn_sol_bfs = Button(830, 325, 106, 40, "BFS")
    btn_sol_dfs = Button(946, 325, 106, 40, "DFS")
    btn_sol_astar = Button(1062, 325, 106, 40, "A*")
    btn_sol_wall = Button(830, 375, 160, 40, "Wall Follower")
    btn_sol_deadend = Button(1010, 375, 160, 40, "Dead-End")

    # speed slider
    speed_options = [("0.01x", 0.01), ("0.1x", 0.1), ("0.5x", 0.5), ("1x", 1.0), ("5x", 5.0), ("10x", 10.0), ("100x", 100.0)]
    speed_slider = SteppedSlider(830, 465, 200, 8, speed_options, 3)
    step_accumulator = 0.0


    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            speed_slider.handle_event(event)

            # algorithm selectors logic 
            if btn_gen_dfs.is_clicked(event) and current_generator != "DFS": current_generator = "DFS"
            if btn_gen_prim.is_clicked(event) and current_generator != "Prim": current_generator = "Prim"
            if btn_gen_kruskal.is_clicked(event) and current_generator != "Kruskal": current_generator = "Kruskal"
            if btn_gen_wilson.is_clicked(event) and current_generator != "Wilson": current_generator = "Wilson"
            
            if btn_sol_bfs.is_clicked(event) and current_solver != "BFS": current_solver = "BFS"
            if btn_sol_dfs.is_clicked(event) and current_solver != "DFS": current_solver = "DFS"
            if btn_sol_astar.is_clicked(event) and current_solver != "A*": current_solver = "A*"
            if btn_sol_wall.is_clicked(event) and current_solver != "Wall Follower": current_solver = "Wall Follower"
            if btn_sol_deadend.is_clicked(event) and current_solver != "Dead-End": current_solver = "Dead-End"
            
            #  size Buttons logic 
            new_size = None
            if btn_s.is_clicked(event): new_size = "S"
            if btn_m.is_clicked(event): new_size = "M"
            if btn_l.is_clicked(event): new_size = "L"
            if btn_xl.is_clicked(event): new_size = "XL"

            # if a size button was clicked, reset
            if new_size and new_size != current_size:
                current_size = new_size
                tile_size = sizes[current_size]
                grid_cells, cols, rows = init_grid(tile_size)

                start_cell = grid_cells[0]
                end_cell = grid_cells[-1]
                start_cell.is_start = True
                end_cell.is_end = True
                
                active_generator = DFSGenerator(start_cell, cols, rows)

                is_generating = False
                is_solving = False
                current_solver_head = None

                # reset analytics
                scanned_count = 0
                path_count = 0
                efficiency = 0
                final_status_text = "Idle"

            # generate button event
            if btn_generate.is_clicked(event):
                # reset grid for a new maze
                grid_cells, cols, rows = init_grid(tile_size)
                start_cell = grid_cells[0]
                end_cell = grid_cells[-1]
                start_cell.is_start = True
                end_cell.is_end = True

                print(f"\n>>> Starting Maze Generation using {current_generator} <<<")


                # call chosen generator algorithm
                if current_generator == "DFS":
                    active_generator = DFSGenerator(start_cell, cols, rows)
                elif current_generator == "Prim":
                    active_generator = PrimGenerator(start_cell, cols, rows)
                elif current_generator == "Kruskal":
                    active_generator = KruskalGenerator(start_cell, cols, rows)
                elif current_generator == "Wilson":
                    active_generator = WilsonGenerator(start_cell, cols, rows)
                
                is_generating = True
                is_solving = False
                current_solver_head = None
                
                # start analytics timer
                scanned_count = 0
                path_count = 0
                efficiency = 0
                final_status_text = ""
                start_time = pygame.time.get_ticks()
            
            if btn_solve.is_clicked(event):
                if not is_generating: # solve when maze is ready
                    # reset cell states
                    for cell in grid_cells:
                        cell.is_scanned = False
                        cell.is_path = False
                    
                    print(f"\n>>> Starting Maze Solving using {current_solver} <<<")

                        
                    # call chosen solver algorithm 
                    if current_solver == "BFS":
                        active_solver = BFSSolver(start_cell, end_cell, cols, rows)
                    elif current_solver == "DFS":
                        active_solver = DFSSolver(start_cell, end_cell, cols, rows)
                    elif current_solver == "A*":
                        active_solver = AStarSolver(start_cell, end_cell, cols, rows)
                    elif current_solver == "Wall Follower":
                        active_solver = WallFollowerSolver(start_cell, end_cell, cols, rows)
                    elif current_solver == "Dead-End":
                        active_solver = DeadEndSolver(start_cell, end_cell, cols, rows)

                    is_solving = True
                    current_solver_head = start_cell

                    # start analytics timer
                    scanned_count = 0
                    path_count = 0
                    efficiency = 0
                    final_status_text = ""
                    start_time = pygame.time.get_ticks()
        
        # Game logic

        steps_this_frame = 0
        if is_generating or is_solving:
            step_accumulator += speed_slider.get_value()
            steps_this_frame = int(step_accumulator)
            step_accumulator -= steps_this_frame

        # 1. maze generator logic
        if is_generating:
            # recursive calling 
            for _ in range(steps_this_frame):
                result_cell = active_generator.step(grid_cells)
                
                if result_cell is None:
                    is_generating = False 
                    print("Maze Generation Complete.")
                    
                    # record end-time
                    elapsed = pygame.time.get_ticks() - start_time
                    final_status_text = f"Generated - {elapsed}ms"
                    break
        
        # 2. maze solver logic
        if is_solving:
            # live update scanned count!
            if active_solver:
                scanned_count = len(active_solver.visited)

            for _ in range(steps_this_frame):
                current_processed = active_solver.step(grid_cells)

                if current_processed is not None:
                    current_solver_head = current_processed # save the active head

                if current_processed is None:  
                    is_solving = False
                    current_solver_head = None
                    print("No Path Possible.")
                    
                    elapsed = pygame.time.get_ticks() - start_time
                    final_status_text = f"No Path - {elapsed}ms"
                    break
                elif current_processed == end_cell:  
                    is_solving = False
                    current_solver_head = None
                    print("Path Found!")
                    
                    elapsed = pygame.time.get_ticks() - start_time
                    final_status_text = f"Solved - {elapsed}ms"

                    temp = end_cell
                    # backtracking path with object's parent map
                    while temp is not None:
                        temp.is_path = True
                        path_count += 1 # count path length
                        temp = active_solver.parent_map.get(temp)
                    
                    # calculate final efficiency
                    if scanned_count > 0:
                        efficiency = int((path_count / scanned_count) * 100)
                    break


        # Visuals
        screen.fill(GREY)
        # draw grid
        for cell in grid_cells:
            cell.draw(screen)
        
        # highlight the Head
        if is_generating and active_generator.current_cell:
            x = active_generator.current_cell.x * tile_size
            y = active_generator.current_cell.y * tile_size
            pygame.draw.rect(screen, (20, 240, 20), (x, y, tile_size, tile_size))
            
        elif is_solving and current_solver_head:
            x = current_solver_head.x * tile_size
            y = current_solver_head.y * tile_size
            pygame.draw.rect(screen, (245, 194, 231), (x, y, tile_size, tile_size))

        # draw the controls n sidebar
        draw_sidebar(screen)
        
        # draw title
        title_surf = title_font.render("PATHFINDER", True, TEXT_COLOUR)
        title_rect = title_surf.get_rect(center=(1000, 35)) 
        screen.blit(title_surf, title_rect)

        # find current status for the status badge
        current_status_text = final_status_text
        current_status_color = STATUS_IDLE
        
        if is_generating:
            current_status_text = "Generating..."
            current_status_color = STATUS_GEN
        elif is_solving:
            current_status_text = "Solving..."
            current_status_color = STATUS_SOLVING
        elif "Solved" in current_status_text:
            current_status_color = STATUS_SOLVED

        # draw bottom status bar with LIVE data
        draw_status_bar(screen, status_text=current_status_text, status_color=current_status_color, scanned=scanned_count, path=path_count, efficiency=efficiency)

        # draw size ui elements
        size_label = ui_font.render("Maze Size", True, TEXT_COLOUR)
        screen.blit(size_label, (830, 70))
        
        btn_s.draw(screen, is_active=(current_size == "S"))
        btn_m.draw(screen, is_active=(current_size == "M"))
        btn_l.draw(screen, is_active=(current_size == "L"))
        btn_xl.draw(screen, is_active=(current_size == "XL"))

        # draw speed ui elements
        speed_label = ui_font.render("Animation Speed", True, TEXT_COLOUR)
        screen.blit(speed_label, (830,430))
        speed_slider.draw(screen)
        # draw algo ui elements
        gen_label = ui_font.render("Generator Algorithm", True, TEXT_COLOUR)
        screen.blit(gen_label, (830, 160))
        btn_gen_dfs.draw(screen, is_active=(current_generator == "DFS"))
        btn_gen_prim.draw(screen, is_active=(current_generator == "Prim"))
        btn_gen_kruskal.draw(screen, is_active=(current_generator == "Kruskal"))
        btn_gen_wilson.draw(screen, is_active=(current_generator == "Wilson"))

        sol_label = ui_font.render("Solver Algorithm", True, TEXT_COLOUR)
        screen.blit(sol_label, (830, 295))
        btn_sol_bfs.draw(screen, is_active=(current_solver == "BFS"))
        btn_sol_dfs.draw(screen, is_active=(current_solver == "DFS"))
        btn_sol_astar.draw(screen, is_active=(current_solver == "A*"))
        btn_sol_wall.draw(screen, is_active=(current_solver == "Wall Follower"))
        btn_sol_deadend.draw(screen, is_active=(current_solver == "Dead-End"))

        btn_generate.draw(screen)
        btn_solve.draw(screen)

        from ui import draw_legend
        draw_legend(screen, 830, 570)

        pygame.display.flip() 
        await asyncio.sleep(0) # .give control back to the browser every frame
        clock.tick(FPS) # limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())  # .run the async main function