from collections import deque

start = (
    (4, 8, 1),
    (6, 3, 0),
    (2, 7, 5)
)

goal = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_next(state):
    x, y = find_zero(state)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    result = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            result.append(tuple(tuple(row) for row in new_state))
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

def DFS(start, goal, limit=20):
    stack = [(start, 0)]
    parent = {start: None}

    while stack:
        current, depth = stack.pop()
        if current == goal:
            break
        if depth >= limit:
            continue
        for nxt in get_next(current):
            if nxt not in parent:
                parent[nxt] = current
                stack.append((nxt, depth + 1))

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
for step in bfs_path:
    print(step)

print("\n===== DFS =====")
print("So buoc DFS:", len(dfs_path) - 1)
for step in dfs_path:
    print(step)
