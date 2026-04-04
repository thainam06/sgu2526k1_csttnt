from collections import deque

maze = [
    ['S', 0, 1, 0, 0],
    [1,   0, 1, 0, 1],
    [0,   0, 0, 0, 1],
    [0,   1, 1, 0, 0],
    [0,   0, 0, 1, 'A']
]

ROWS = len(maze)
COLS = len(maze[0])

def find_pos(value):
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == value:
                return (i, j)

start = find_pos('S')
goal  = find_pos('A')
def get_next(pos):
    x, y = pos
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    result = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            if maze[nx][ny] != 1:
                result.append((nx, ny))
    return result
def BFS(start, goal):
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for nxt in get_next(current):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)

    if goal not in parent:
        return []

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]
def DFS(start, goal):
    stack = [start]
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        for nxt in get_next(current):
            if nxt not in parent:
                parent[nxt] = current
                stack.append(nxt)

    if goal not in parent:
        return []

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]
bfs_path = BFS(start, goal)
dfs_path = DFS(start, goal)

print("===== BFS =====")
print("So buoc BFS:", len(bfs_path) - 1)
print("Duong di BFS:", bfs_path)

print("\n===== DFS =====")
print("So buoc DFS:", len(dfs_path) - 1)
print("Duong di DFS:", dfs_path)
