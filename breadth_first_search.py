from global_objects import *
from utility import *

class BFS:
    def __init__(self):
        self.name = "BFS"
    
    def run(self, grid):
        start_cell = grid.start_flag_cell
        x,y = start_cell.get_array_pos()

        queue = deque()
        visit = set()
        queue.append((x,y))
      
        while queue:
            x,y = queue.popleft()
            
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
                i,j = n
                if not check_out_of_bounds(grid, i, j):
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell not in visit:
                    queue.append(n)
                    neighbor_cell.prev = cell

            grid.draw()
            pygame.display.update()
            clock.tick(80)
        
        # Draw final path
        draw_final_path(grid)