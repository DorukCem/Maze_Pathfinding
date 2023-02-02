from global_objects import *

class DFS:
    def __init__(self):
        self.name = "DFS"
    
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
                if i<0 or j<0 or i>=len(grid.array) or j>=len(grid.array[0]): #Check out of bounds
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell not in visit:
                    queue.appendleft(n)
                    neighbor_cell.prev = cell

            grid.draw()
            pygame.display.update()
            clock.tick(80)
        
        #draw final path
        if grid.end_flag_cell.prev:
            cell = grid.end_flag_cell
            while cell.prev:
                cell.color = FINAL_PATH_COLOR
                cell = cell.prev
                
            grid.start_flag_cell.color = FINAL_PATH_COLOR