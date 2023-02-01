from global_objects import*

class Cell:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.border_color = BORDER_COLOR
      self.color = DEFAULT_COLOR
      self.flag = None
      self.is_filled = False
      self.prev = None
      
   def __repr__(self):
      return ""#str(self.x) + " " + str(self.y)
   
   def __lt__(self, other):
        return other
   
   def get_array_pos(self):
      return (int(self.y/CELL_SIZE), int(self.x/CELL_SIZE))

   def get_neighbors_coords(self):
      x,y = self.get_array_pos()
      return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
   

class Grid:
   def __init__(self):
      self.width = WIDTH
      self.height = WIDTH
      self.array = [[Cell(i, j) for i in range(0, WIDTH, CELL_SIZE)] for j in range(0, HEIGHT, CELL_SIZE)]
      
      self.start_flag_cell = None
      self.end_flag_cell = None
      self.setup_flags()

      self.cell_that_switched_last = None # So that cells do not flicker

   def setup_flags(self):
      x = int(GRIDWITH/2)
      y = int(GRIDHEIGHT/2)
      self.array[y][x].flag = "Start"
      self.array[y][x+1].flag = "End"
      self.start_flag_cell = self.array[y][x]
      self.end_flag_cell = self.array[y][x+1]

   def reset_grid(self):
      for row in self.array:
         for cell in row:
            if cell.is_filled == False: 
               cell.color = DEFAULT_COLOR
            cell.prev = None

   def get_cell_being_clicked(self, coordinate):
      x,y = coordinate
      cell_index_x = x//CELL_SIZE
      cell_index_y = y//CELL_SIZE
      return self.array[cell_index_y][cell_index_x]
   
   def change_flag_position(self, flag, position):
      cell_clicked = self.get_cell_being_clicked(position)
      if cell_clicked.flag != None or cell_clicked.is_filled:
         return
      if flag == "End":
            self.end_flag_cell.flag = None
            self.end_flag_cell = cell_clicked
            cell_clicked.flag = "End"
            self.end_flag_cell = cell_clicked
      else:
            self.start_flag_cell.flag = None
            self.start_flag_cell = cell_clicked
            cell_clicked.flag = "Start"
            self.start_flag_cell = cell_clicked

   def draw(self):
      for row in self.array:
         for cell in row:
            x,y = cell.x, cell.y
            pygame.draw.rect(screen, cell.color , (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, cell.border_color, (x, y, CELL_SIZE, CELL_SIZE), 1)
            if cell.flag == "Start":
               screen.blit(start_flag_surface, (x, y))
            if cell.flag == "End":
               screen.blit(end_flag_surface, (x, y))