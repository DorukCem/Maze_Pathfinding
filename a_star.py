from global_objects import *
import math
import heapq

class A_star:
    def __init__(self):
        self.name = "A*"
        self.start = None
        self.end = None

    def distance_from_end(self, cell):
        #Since we are only doing comparisions with the distance, we can just compare them with finding the square root
        #a2 > b2 -> a > b
        return (self.end.x - cell.x)**2 + (self.end.y  - cell.y )**2      #h(x)
                                              
    def distance_between_cells(self, cell1, cell2):
        return (cell1.x -cell2.x)**2 + (cell1.y - cell2.y)**2
    

    def run(self, grid):
        self.start = grid.start_flag_cell
        self.end = grid.end_flag_cell
        
        open = []
        closed = set()
        heapq.heappush(open, (self.distance_from_end(self.start) ,self.start) ) #We pass in as (distance, cell) so that the heap is sorted by distance
        self.start.distance_from_start = 0

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
                
                new_dist = cell.distance_from_start + self.distance_between_cells(cell, neighbor_cell) #g(x)
                if new_dist < neighbor_cell.distance_from_start:
                    neighbor_cell.prev = cell
                    neighbor_cell.distance_from_start = new_dist
                if neighbor_cell.prev == None:
                    neighbor_cell.prev = cell
                
                neighbor_cell.distance_from_end = self.distance_from_end(neighbor_cell) #h(x)
                evaluation = neighbor_cell.distance_from_end + neighbor_cell.distance_from_start #f(x) = g(x) + h(x)
                neighbor_cell.color = "Pink"
                heapq.heappush(open, (evaluation , neighbor_cell))

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
