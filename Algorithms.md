# 🧠 Algorithms 

This project visualizes how computers "think" when navigating space. Below is a breakdown of the algorithms used to generate and solve the mazes.

---

## 🏗️ Maze Generation

These algorithms start with a grid full of walls and carve out paths to create a perfect maze (where every point is reachable, but there are no loops).

### 1. Recursive Backtracker
**Type:** Depth-First Search (DFS)
**Style:** Long, winding corridors.

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


---

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

### 2. Depth-First Search (DFS)
**Type:** Unweighted Search
**Guarantee:** Does NOT guarantee the shortest path.

**How it works:**
* DFS is like a person walking in a maze with their hand on the left wall.
* It picks a path and keeps walking until it hits a dead end.
* Then it backtracks and tries the next available turn.

**Pros/Cons:** It can be very fast if it gets lucky, but it often finds a winding, inefficient path.

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

---

## 📚 Definitions

* **Node/Cell:** A single square in the grid.
* **Edge:** The connection between two cells (if there is no wall).
* **Stack:** A "Last-In, First-Out" data structure (like a stack of plates). Used for DFS and Backtracking.
* **Queue:** A "First-In, First-Out" data structure (like a line at a store). Used for BFS.