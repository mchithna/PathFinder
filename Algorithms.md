# 🧠 Algorithms 

This project visualizes how computers "think" when navigating space. Below is a breakdown of the algorithms used to generate and solve the mazes.

---

## 🏗️ Maze Generation

These algorithms start with a grid full of walls and carve out paths to create a perfect maze (where every point is reachable, but there are no loops).

### 1. Recursive Backtracker (DFS)
**Type:** Depth-First Search (DFS)
**Style:** Long, winding corridors with directional bias.

**How it works:**
1.  **Choose a starting cell** and mark it as visited.
2.  **Look around** for unvisited neighbors (Top, Right, Bottom, Left).
3.  **If a neighbor is found:**
    * Knock down the wall between the current cell and the neighbor.
    * Move to that neighbor.
    * Add the current spot to a "Stack" (a breadcrumb trail).
4.  **If NO neighbor is found (Dead End):**
    * Backtrack! Pop the last cell off the stack and go back there.
    * Repeat until you find a cell with unvisited neighbors.

**Performance:** Fast and memory-efficient.

---
![dfs](assets/dfs.gif)

### 2. Prim's Algorithm
**Type:** Spanning Tree Growth
**Style:** Bushy mazes with many dead-ends and a centred bias.

**How it works:**
* Start with a random cell already in the "maze."
* Look at all **walls** adjacent to cells already in the maze.
* Pick a random wall from this list.
* If the wall connects to an unvisited cell, knock it down and add that cell to the maze.
* Repeat until all cells are part of the maze.

**The Analogy:** Imagine a forest growing outward from a seed. Trees expand in all directions, creating a dense, bushy pattern.

**Performance:** Balanced and produces aesthetically pleasing mazes.

---
![prim](assets/prim.gif)

### 3. Kruskal's Algorithm
**Type:** Disjoint Set Union (Union-Find)
**Style:** Perfectly uniform, unbiased mazes.

**How it works:**
* Start with every cell in its own isolated group.
* List all walls in the maze.
* Shuffle the walls randomly.
* For each wall:
    * Check if it connects two cells from **different groups**.
    * If yes, knock down the wall and **merge** the two groups.
    * If no, skip it.
* Continue until all cells are connected (one group).

**The Analogy:** Imagine separate islands merging together by removing walls between them. Eventually, all islands become one continent.

**Performance:** Creates statistically random, unbiased mazes.

---
![kruskal](assets/kruskal.gif)

### 4. Wilson's Algorithm
**Type:** Loop-Erased Random Walk
**Style:** Perfectly uniform spanning tree (the gold standard).

**How it works:**
* Start with one random cell in the maze.
* Pick an unvisited cell and start a random walk from it.
* Walk randomly until you either:
    * Hit a cell already in the maze → **erase the loop** you created and add the entire path to the maze.
    * Return to your starting cell → erase the loop and try again.
* Repeat until all cells are in the maze.

**The Analogy:** Like a drunken person walking around until they find their way home. Once they find home, we redraw their path without any silly loops.

**Performance:** Slower to start but produces the most statistically uniform mazes.

---
![wilson](assets/wilson.gif)

## 🧩 Maze Solving

Once the maze is built, these algorithms search for the shortest path from the **Start Node** (Green) to the **End Node** (Red).

### 1. Breadth-First Search (BFS)
**Type:** Unweighted Search

**Guarantee:** Always finds the Shortest Path.

**How it works:**
* Imagine pouring water into the maze at the Start.
* The water flows into every open hallway equally, expanding in all directions at the same speed.
* The moment the water touches the End Node, we trace the flow back to the start.

**Visuals:**
* **Blue:** Cells being scanned (the "water").
* **Yellow:** The final shortest path.

![s-bfs](assets/s-bfs.gif)

### 2. Depth-First Search (DFS)
**Type:** Unweighted Search
**Guarantee:** Does NOT guarantee the shortest path.

**How it works:**
* DFS is like a person walking in a maze with their hand on the left wall.
* It picks a path and keeps walking until it hits a dead end.
* Then it backtracks and tries the next available turn.

**Pros/Cons:** It can be very fast if it gets lucky, but it often finds a winding, inefficient path.

![s-dfs](assets/s-dfs.gif)

### 3. A* (A-Star) Search
**Type:** Weighted Search + Heuristic
**Guarantee:** Always finds the Shortest Path (and usually faster than BFS).

**How it works:**
* A* is "smart." It doesn't just look everywhere like BFS.
* It uses a **Heuristic** (a guess) to estimate which cells are closer to the End Node.
* It prioritizes checking cells that move *towards* the goal, acting like a guided missile rather than a flood.

**Formula:** `f(n) = g(n) + h(n)`
* `g(n)` = Distance from Start.
* `h(n)` = Estimated distance to End (Manhattan Distance).

**Performance:** Most efficient on large mazes; skips many unnecessary cells.

---
![s-astar](assets/s-astar.gif)

### 4. Wall Follower
**Type:** Deterministic Following
**Guarantee:** Finds the exit (but may not find the shortest path).

**How it works:**
* Imagine your **right hand is on the right wall** of the maze.
* Walk forward while keeping your hand on the wall.
* Your hand will follow the wall's contours, guiding you through the maze.
* Eventually, you'll reach the exit.

**The Analogy:** This is like the classic "hand on the wall" trick people use to escape mazes by touch alone.

**Limitation:** Only works on **simply-connected mazes** (mazes without loops within loops). In complex mazes, you might end up back where you started.

**Performance:** Very fast and intuitive to visualize.

---
![s-wall](assets/s-wall.gif)

### 5. Dead-End Filling
**Type:** Elimination Method
**How it works:**
* Start from outside the maze and identify all **dead-ends**.
* "Fill in" (mark as invalid) each dead-end cell.
* Move inward, continuing to fill dead-ends.
* The remaining path is guaranteed to be the solution.

**The Analogy:** Like trimming branches from a tree. You keep cutting off the dead-end twigs until only the main trunk (the solution) remains.

**Guarantee:** Always finds the shortest path.
**Performance:** Elegant and efficient; processes cells level by level from the boundaries inward.

---
![s-dead](assets/s-dead.gif)

## 📚 Definitions

* **Node/Cell:** A single square in the grid.
* **Edge:** The connection between two cells (if there is no wall).
* **Stack:** A "Last-In, First-Out" data structure (like a stack of plates). Used for DFS and Backtracking.
* **Queue:** A "First-In, First-Out" data structure (like a line at a store). Used for BFS.
