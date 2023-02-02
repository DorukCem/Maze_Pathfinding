from settings import *

class Cell:
   def __init__(self, x, y):
      # x,y are pygame coordinates and should not be confues with array position
      self.x = x                     
      self.y = y
      self.border_color = BORDER_COLOR
      self.color = DEFAULT_COLOR
      self.flag = None
      self.is_filled = False
      self.prev = None
      
      # for A*
      self.distance_from_end = None
      self.distance_from_start = float('inf')

   def __repr__(self):
      return ""
   
   def __lt__(self, other): # overload comparision so that same priorty elements can break ties
        return other
   
   def get_array_pos(self):                                    #get index of cell 
      return (int(self.y/CELL_SIZE), int(self.x/CELL_SIZE))

   def get_neighbors_coords(self):
      x,y = self.get_array_pos()
      return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]