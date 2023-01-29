from settings import *

REGULAR = 1
START = 2
END = 3

class Cell:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.border_color = "Red"
      self.color = "Blue"
      self.property = REGULAR        #Bad name
      
   
   def __repr__(self):
      return str(self.x) + " " + str(self.y)

class Grid:
   def __init__(self):
      self.width = WIDTH
      self.height = WIDTH
      self.array = [[Cell(i, j) for i in range(0, WIDTH, CELL_SIZE)] for j in range(0, HEIGHT, CELL_SIZE)]

   def get_cell_being_clicked(self, coordinate):
      x,y = coordinate
      cell_index_x = x//CELL_SIZE
      cell_index_y = y//CELL_SIZE
      return self.array[cell_index_y][cell_index_x]
