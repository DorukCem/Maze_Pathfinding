from global_objects import *
import math
import heapq

def distance_between_cells(cell1, cell2):
        return (cell1.x -cell2.x)**2 + (cell1.y - cell2.y)**2

def is_new_distance_better(new_distance, cell):
    if new_distance < cell.distance_from_start:
        return True
    return False


class A_star:
    def __init__(self):
        self.name = "A*"
        self.start = None
        self.end = None
    
    def run(self, grid):
        self.start = grid.start_flag_cell
        self.end = grid.end_flag_cell
        
        open = []
        closed = set()
        distance = distance_between_cells(self.start, self.end)
        heapq.heappush(open, (distance, self.start)) #We pass in as (distance, cell) so that the heap is sorted by distance
        self.start.distance_from_start = 0

        while open:
            _ , cell = heapq.heappop(open) #(distance, cell)
            if cell.flag == "End":
                break

            closed.add(cell)
            cell.color = HAS_BEEN_SEARCHED_COLOR

            neighbors = cell.get_neighbors_coords()
            for n in neighbors:
                i,j = n
                if i<0 or j<0 or i>=len(grid.array) or j>=len(grid.array[0]): #Check out of bounds
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell in closed or neighbor_cell.is_filled:
                    continue
                
                new_distance = cell.distance_from_start + distance_between_cells(cell, neighbor_cell) #g(x)
                if is_new_distance_better(new_distance, neighbor_cell):
                    neighbor_cell.distance_from_start = new_distance
                    neighbor_cell.prev = cell
                
                if neighbor_cell.distance_from_end == None:
                    neighbor_cell.distance_from_end = distance_between_cells(neighbor_cell, self.end) #h(x)
                evaluation = neighbor_cell.distance_from_end + neighbor_cell.distance_from_start #f(x) = g(x) + h(x)
                
                heapq.heappush(open, (evaluation , neighbor_cell)) 
                neighbor_cell.color = APPEND_COLOR

            grid.draw()
            pygame.display.update()
            clock.tick(80)
        
        #Draw final path
        if grid.end_flag_cell.prev:
            cell = grid.end_flag_cell
            while cell.prev:
                cell.color = FINAL_PATH_COLOR
                cell = cell.prev
                
            grid.start_flag_cell.color = FINAL_PATH_COLOR

# We are replacing previus nodes even when the path is longer
