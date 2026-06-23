import time
import os
from collections import deque

# ─── Maze Layout ───────────────────────────────────────────────
# 0 = open path, 1 = wall, S = start, E = end
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

START = (1, 1)
END   = (13, 13)

# ─── Colors ────────────────────────────────────────────────────
RESET  = "\033[0m"
WALL   = "\033[40m  \033[0m"        # black
PATH   = "\033[47m  \033[0m"        # white
VISIT  = "\033[44m  \033[0m"        # blue  - explored
FOUND  = "\033[42m  \033[0m"        # green - final path
START_ = "\033[41m S\033[0m"        # red   - start
END_   = "\033[45m E\033[0m"        # purple- end

def draw(maze, visited, path_set, title=""):
    os.system("clear")
    print(f"\n  {title}\n")
    for r, row in enumerate(maze):
        line = "  "
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == START:
                line += START_
            elif pos == END:
                line += END_
            elif pos in path_set:
                line += FOUND
            elif pos in visited:
                line += VISIT
            elif cell == 1:
                line += WALL
            else:
                line += PATH
        print(line)
    print()

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(START)
    return set(path)

# ─── BFS ───────────────────────────────────────────────────────
def bfs(maze):
    queue = deque([START])
    visited = {START}
    came_from = {}
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    print("\033[?25l")  # hide cursor
    while queue:
        r, c = queue.popleft()

        if (r, c) == END:
            path = reconstruct_path(came_from, END)
            draw(maze, visited, path, "BFS — Shortest Path Found! 🎉")
            print(f"  ✅ Path length: {len(path)} steps\n")
            print("\033[?25h")  # show cursor
            return

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    came_from[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

        draw(maze, visited, set(), f"BFS — Exploring... ({len(visited)} cells visited)")
        time.sleep(0.05)

    print("No path found!")
    print("\033[?25h")

# ─── DFS ───────────────────────────────────────────────────────
def dfs(maze):
    stack = [START]
    visited = {START}
    came_from = {}
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    print("\033[?25l")
    while stack:
        r, c = stack.pop()

        if (r, c) == END:
            path = reconstruct_path(came_from, END)
            draw(maze, visited, path, "DFS — Path Found! 🎉")
            print(f"  ✅ Path length: {len(path)} steps\n")
            print("\033[?25h")
            return

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    came_from[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

        draw(maze, visited, set(), f"DFS — Exploring... ({len(visited)} cells visited)")
        time.sleep(0.05)

    print("No path found!")
    print("\033[?25h")

# ─── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🧠 Maze Solver — DSA + AI Visualizer")
    print("=====================================")
    print("  🟥 Red   = Start")
    print("  🟣 Purple = End")
    print("  🟦 Blue  = Cells being explored")
    print("  🟩 Green = Final path found")
    print("  ⬛ Black = Wall")
    print()
    print("Choose algorithm:")
    print("  1. BFS (Breadth First Search) — always finds SHORTEST path")
    print("  2. DFS (Depth First Search)   — faster but not always shortest")
    print()

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        bfs(MAZE)
        print("  💡 BFS explores level by level — guarantees shortest path.\n")
    elif choice == "2":
        dfs(MAZE)
        print("  💡 DFS goes deep first — faster but may not find shortest path.\n")
    else:
        print("Invalid choice!")