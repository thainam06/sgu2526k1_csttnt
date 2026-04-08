def read_puzzle_file(filename):
    try:
        with open(filename, 'r') as f:
            # Đọc tất cả các dòng, loại bỏ khoảng trắng thừa và dòng trống
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return None, None

        # Chuyển đổi các dòng còn lại thành ma trận số nguyên
        matrix_data = [list(map(int, line.split())) for line in lines[0:]]

        # Tách 3 dòng đầu và 3 dòng cuối
        start_state = matrix_data[:3]
        goal_state = matrix_data[3:6]  # Lấy 3 dòng tiếp theo

        return start_state, goal_state

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file")
        return None, None


def find_blank(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
    return None

import copy

def get_neighbors(state):
    neighbors = []
    r, c = find_blank(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lên, Xuống, Trái, Phải

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            # Sao chép ma trận và hoán đổi vị trí
            new_state = copy.deepcopy(state)
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(new_state)
    return neighbors

#ham tinh heuristic
def manhattan_distance(current_state, goal_state):
    distance = 0
    # Tạo bản đồ vị trí đích để tra cứu nhanh
    goal_map = {val: (r, c) for r, row in enumerate(goal_state) for c, val in enumerate(row)}

    for r in range(3):
        for c in range(3):
            val = current_state[r][c]
            if val != 0:  # Không tính ô trống
                target_r, target_c = goal_map[val]
                distance += abs(r - target_r) + abs(c - target_c)
    return distance


import heapq


def solve_puzzle(start, goal):
    # (priority, g_score, current_state, path)
    queue = [(manhattan_distance(start, goal), 0, start, [])]
    visited = set()

    while queue:
        f, g, current, path = heapq.heappop(queue)

        if current == goal:
            return path + [current]

        # Chuyển state thành tuple để có thể lưu vào set (vì list không hash được)
        state_tuple = tuple(tuple(row) for row in current)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(current):
            new_path = path + [current]
            h = manhattan_distance(neighbor, goal)
            heapq.heappush(queue, (g + 1 + h, g + 1, neighbor, new_path))

    return None

start, goal = read_puzzle_file('Puzzle.txt')
solution = solve_puzzle(start, goal)

if solution:
    print(f"Tìm thấy lời giải sau {len(solution)-1} bước!")
    for i, step in enumerate(solution):
        print(f"Bước {i}:")
        for row in step: print(row)
        print()
else:
    print("Không có lời giải.")