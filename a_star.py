from time import sleep
from utility import *
import heapq
import pqdict

def distance_between_cells(cell1, cell2):
        return abs(cell1.x -cell2.x) + abs(cell1.y - cell2.y)

def new_distance_is_better(new_distance, cell):
    if cell.distance_from_start == None:
        return True
    if new_distance < cell.distance_from_start:
        return True
    return False


class A_star:
    def __init__(self):
        self.name = "A*"
        
    
    def run(self, grid):
        start = grid.start_flag_cell
        end = grid.end_flag_cell
        
        open_cell = pqdict.pqdict()
        closed = set()
        distance = distance_between_cells(start, end)
        open_cell[start] = distance #We pass in as (distance, cell) so that the heap is sorted by distance
        start.distance_from_start = 0

        while len(open_cell):
            cell = open_cell.pop() 
            if cell.flag == "End":
                break
            
            closed.add(cell)
            cell.color = HAS_BEEN_SEARCHED_COLOR

            neighbors = cell.get_neighbors_coords()
            for n in neighbors:
                i,j = n
                if not check_out_of_bounds(grid, i, j):
                    continue
                neighbor_cell = grid.array[i][j]
                if neighbor_cell in closed or neighbor_cell.is_filled:
                    continue
                
                new_distance = cell.distance_from_start + distance_between_cells(cell, neighbor_cell) #g(x)

                if new_distance_is_better(new_distance, neighbor_cell):
                    neighbor_cell.distance_from_start = new_distance
                    neighbor_cell.prev = cell

                if neighbor_cell.distance_from_end == None:
                    neighbor_cell.distance_from_end = distance_between_cells(neighbor_cell, end) #h(x)

                evaluation = neighbor_cell.distance_from_end + neighbor_cell.distance_from_start #f(x) = g(x) + h(x)
                
                open_cell[neighbor_cell] = evaluation 
                neighbor_cell.color = APPEND_COLOR

            sleep(0.02)
        
        #Draw final path
        draw_final_path(grid)

        

