from global_objects import *
import math
import heapq

class A_star:
    def __init__(self):
        self.name = "A*"
        self.start = None
        self.end = None

    def evaluation_function(self, cell):
        #Since we are only doing comparisions with the distance, we can just compare them with finding the square root
        #a2 > b2 -> a > b
        dist_from_start = (self.start.x - cell.x)**2 + (self.start.y  - cell.y )**2 #g(x)
        dist_from_end =  (self.end.x - cell.x)**2 + (self.end.y  - cell.y )**2      #h(x)
        return (dist_from_start + dist_from_end, dist_from_end)                                                # f(x) = g(x) + h(x)
    
    def run(self, grid):
        self.start = grid.start_flag_cell
        self.end = grid.end_flag_cell
        
        open = []
        closed = set()
        heapq.heappush(open, (self.evaluation_function(self.start) ,self.start)) #We pass in as (distance, cell) so that the heap is sorted by distance
        
        while open:
            _ , cell = heapq.heappop(open)
            if cell.flag == "End":
                cell.color = FINAL_PATH_COLOR
                break
            closed.add(cell)
            cell.color = HAS_BEEN_SEARCHED_COLOR
            neighbors = cell.get_neighbors_coords()
            for n in neighbors:
                i,j = n
                if i<0 or j<0 or i>=len(grid.array) or j>=len(grid.array[0]):
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell in closed or neighbor_cell.is_filled:
                    continue
                neighbor_cell.prev = cell
                distance = self.evaluation_function(neighbor_cell)
                heapq.heappush(open, (distance , neighbor_cell))

            grid.draw()
            pygame.display.update()
            clock.tick(20)
        
        if grid.end_flag_cell.prev:
            cell = grid.end_flag_cell.prev
            while cell.prev:
                cell.color = FINAL_PATH_COLOR
                cell = cell.prev
                
            grid.start_flag_cell.color = FINAL_PATH_COLOR

# We are replacing previus nodes even when the path is longer
