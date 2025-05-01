from collections import deque
from time import sleep
from utility import *


class DFS:
    def __init__(self):
        self.name = "DFS"

    def run(self, grid):
        start_cell = grid.start_flag_cell
        x, y = start_cell.get_array_pos()

        queue = deque()
        visit = set()
        queue.append((x, y))

        while queue:
            if grid.kill_thread:
                grid.kill_thread = False
                return

            x, y = queue.popleft()

            cell = grid.array[x][y]
            if cell in visit:
                continue
            visit.add(cell)
            if cell.is_filled:
                continue

            if cell.flag == "End":
                break

            cell.color = HAS_BEEN_SEARCHED_COLOR
            neighbors = cell.get_neighbors_coords()
            for n in neighbors:
                i, j = n
                if not check_out_of_bounds(grid, i, j):
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell not in visit:
                    queue.appendleft(n)
                    neighbor_cell.prev = cell

            sleep(0.02)

        # draw final path
        draw_final_path(grid)
