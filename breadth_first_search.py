from global_objects import *

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
            if x<0 or y<0 or x>=len(grid.array) or y> len(grid.array[0]):
                continue
            cell = grid.array[x][y]
            if cell in visit:
                continue
            visit.add(cell)
            if cell.is_filled:
                continue

            if cell.flag == "End":
                cell.color = "Red"
                break

            cell.color = HAS_BEEN_SEARCHED_COLOR
            neighbors = cell.get_neighbors_coords()
            for n in neighbors:
                if n not in visit:
                    queue.append(n)

            grid.draw()
            pygame.display.update()
            clock.tick(20)
        
        
            