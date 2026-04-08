import time
from collections import deque

# --- 1. Khởi tạo môi trường ---
# ROWS, COLS = 6, 6
# start_pos = (0, 0)
# goal_pos = (5, 5)
#
# walls = [
#     ((0, 1), (0, 2)), ((1, 1), (1, 2)),
#     ((4, 1), (4, 2)), ((5, 1), (5, 2)),
#     ((2, 4), (3, 4)), ((2, 5), (3, 5))
# ]

def read_maze_simple(filename):
    try:
        with open(filename, 'r') as f:
            # Đọc từng dòng, chuyển tất cả con số thành list số nguyên
            data = [list(map(int, line.split())) for line in f if line.strip()]

        if not data: return None

        # Dòng 0: Kích thước
        rows, cols = data[0][0], data[0][1]

        # Dòng 1: Start (x,y) và Goal (x,y)
        # data[1] là [0, 0, 5, 5]
        start_pos = (data[1][0], data[1][1])
        goal_pos = (data[1][2], data[1][3])

        # Các dòng còn lại: Tường (x1, y1, x2, y2)
        walls = []
        for line in data[2:]:
            # Gom [x1, y1, x2, y2] thành ((x1, y1), (x2, y2))
            wall_pair = ((line[0], line[1]), (line[2], line[3]))
            walls.append(wall_pair)

        return rows, cols, start_pos, goal_pos, walls

    except FileNotFoundError:
        print("Không tìm thấy file!")
        return None


# --- 2. Các hàm bổ trợ ---
def is_valid(current, next_node, walls, rows, cols):
    r, c = next_node
    if not (0 <= r < rows and 0 <= c < cols):
        return False
    if (current, next_node) in walls or (next_node, current) in walls:
        return False
    return True


def reconstruct_path(visited, start, goal):
    if goal not in visited: return None
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    return path[::-1]


import heapq


def heuristic(a, b):
    # Sử dụng khoảng cách Manhattan: |x1 - x2| + |y1 - y2|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, goal, walls, rows, cols):
    # Priority Queue lưu trữ các bộ: (độ ưu tiên f, node hiện tại)
    # Priority Queue mặc định của Python là min-heap
    pq = []
    heapq.heappush(pq, (0, start))

    # Lưu vết đường đi: {node: parent_node}
    came_from = {start: None}

    # Lưu chi phí g(n): {node: cost}
    cost_so_far = {start: 0}

    while pq:
        # Lấy node có f(n) thấp nhất
        current_f, current = heapq.heappop(pq)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_node = (current[0] + dr, current[1] + dc)

            if is_valid(current, next_node, walls, rows, cols):
                # Trong lưới ô vuông đơn giản, chi phí mỗi bước là 1
                new_cost = cost_so_far[current] + 1

                # Nếu node chưa đi qua HOẶC tìm được đường đi rẻ hơn đến node này
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    # f(n) = g(n) + h(n)
                    priority = new_cost + heuristic(next_node, goal)
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current

    return None


# --- 4. Hàm xuất thứ tự đi và Kiểm tra thời gian ---
def print_path(path, name="Thuật toán"):
    if path:
        print(f"--- {name}: ({len(path) - 1} bước) ---")
        print(" -> ".join([str(p) for p in path]))
    else:
        print(f"--- {name}: Không tìm thấy đường đi! ---")


def benchmark(algo_func, name, *args):
    start_time = time.perf_counter()
    result = algo_func(*args)
    end_time = time.perf_counter()

    duration_ms = (end_time - start_time) * 1000
    print(f"\n[Thời gian chạy {name}]: {duration_ms:.4f} ms")
    return result


import matplotlib.pyplot as plt


def visualize_maze(path, walls, rows, cols, title="Maze Path"):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Vẽ lưới ô vuông
    for r in range(rows + 1):
        ax.axhline(r, color='lightgrey', lw=1, zorder=1)
    for c in range(cols + 1):
        ax.axvline(c, color='lightgrey', lw=1, zorder=1)

    # Vẽ tường dựa trên tọa độ hàng/cột (Matrix)
    for (node1, node2) in walls:
        r1, c1 = node1
        r2, c2 = node2
        # Tường dọc: khác nhau ở cột (vẽ đường thẳng đứng tại x = max_col)
        if c1 != c2:
            x = max(c1, c2)
            ax.plot([x, x], [r1, r1 + 1], color='black', lw=5, zorder=3)
        # Tường ngang: khác nhau ở hàng (vẽ đường nằm ngang tại y = max_row)
        elif r1 != r2:
            y = max(r1, r2)
            ax.plot([c1, c1 + 1], [y, y], color='black', lw=5, zorder=3)

    # Vẽ đường đi (Arrow) - Giữ nguyên gốc tọa độ ma trận
    if path:
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            # xy=(x, y) trong đồ thị tương ứng (cột, hàng)
            ax.annotate('', xy=(c2 + 0.5, r2 + 0.5),
                        xytext=(c1 + 0.5, r1 + 0.5),
                        arrowprops=dict(arrowstyle='->', color='blue', lw=2, mutation_scale=15),
                        zorder=4)

    # Đánh dấu Start (Kiến) và Goal (A)
    ax.text(start_pos[1] + 0.5, start_pos[0] + 0.5, '🐜', fontsize=22, ha='center', va='center', zorder=5)
    ax.text(goal_pos[1] + 0.5, goal_pos[0] + 0.5, 'A', fontsize=22, color='red', weight='bold', ha='center',
            va='center', zorder=5)

    # Cấu hình hiển thị: Gốc (0,0) ở TOP-LEFT
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)  # Quan trọng: Đảo ngược trục Y từ rows về 0
    ax.xaxis.tick_top()  # Đưa nhãn trục X lên trên cho giống ma trận
    ax.set_xlabel("Cột (Columns)")
    ax.set_ylabel("Hàng (Rows)")
    plt.title(title, pad=30)
    plt.show()


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_ant(path, walls, rows, cols):
    if not path:
        print("Không có đường đi để tạo animation!")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    def setup_maze():
        ax.clear()
        # Vẽ lưới
        for r in range(rows + 1):
            ax.axhline(r, color='lightgrey', lw=1, zorder=1)
        for c in range(cols + 1):
            ax.axvline(c, color='lightgrey', lw=1, zorder=1)

        # Vẽ tường (Dựa trên tọa độ hàng/cột chuẩn)
        for (node1, node2) in walls:
            r1, c1 = node1
            r2, c2 = node2
            if c1 != c2:  # Tường dọc
                ax.plot([max(c1, c2), max(c1, c2)], [r1, r1 + 1], color='black', lw=5, zorder=3)
            elif r1 != r2:  # Tường ngang
                ax.plot([c1, c1 + 1], [max(r1, r2), max(r1, r2)], color='black', lw=5, zorder=3)

        # Đích A
        ax.text(goal_pos[1] + 0.5, goal_pos[0] + 0.5, 'A', fontsize=22, color='red', weight='bold', ha='center',
                va='center')

        # Cấu hình hệ tọa độ Top-Left
        ax.set_xlim(0, cols)
        ax.set_ylim(rows, 0)
        ax.xaxis.tick_top()
        ax.set_title("Kiến tìm đường tới A", pad=20)

    # Đối tượng con kiến (sẽ di chuyển)
    ant_marker, = [None]  # Placeholder

    def init():
        setup_maze()
        return []

    def update(frame):
        setup_maze()  # Vẽ lại maze để tránh vết cũ (hoặc chỉ vẽ đè)
        r, c = path[frame]
        # Vẽ con kiến tại vị trí hiện tại
        ax.text(c + 0.5, r + 0.5, 'o', fontsize=25, ha='center', va='center', zorder=5)

        # Vẽ lại các bước đã đi (để lộ dấu vết)
        if frame > 0:
            past_path = path[:frame + 1]
            px = [p[1] + 0.5 for p in past_path]
            py = [p[0] + 0.5 for p in past_path]
            ax.plot(px, py, color='blue', alpha=0.3, lw=2, zorder=4)

    # Tạo animation
    # frames: số bước đi, interval: thời gian giữa các bước (ms)
    ani = FuncAnimation(fig, update, frames=len(path), init_func=init, interval=500, repeat=False)

    plt.show()
    # Nếu muốn lưu thành GIF, bỏ comment dòng dưới:
    ani.save('ant_path.gif', writer='pillow')

#khởi tạo
ROWS, COLS, start_pos, goal_pos, walls = read_maze_simple('maze.txt')

# --- Chạy thực tế ---
# path_result = a_star(start_pos,goal_pos,walls,ROWS,COLS)
# animate_ant(path_result, walls, ROWS, COLS)



# --- 5. Thực thi ---
path_result = benchmark(a_star, "A* Search", start_pos, goal_pos, walls, ROWS, COLS)
print_path(path_result, "A*")

# path_result = a_star(start_pos,goal_pos,walls,ROWS,COLS)
# visualize_maze(path_result, walls, ROWS, COLS, "Quá trình di chuyển của con kiến (BFS)")