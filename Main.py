import pygame
from sys import exit
from settings import *
from grid import Grid
 

pygame.init()
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()

def draw_grid(grid):
   for row in grid.array:
         for cell in row:
            x,y = cell.x, cell.y
            pygame.draw.rect(screen, cell.color , (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, cell.border_color, (x, y, CELL_SIZE, CELL_SIZE), 1)
            if cell.flag == "Start":
               pygame.draw.rect(screen, "Red" , (x, y, CELL_SIZE, CELL_SIZE))
            if cell.flag == "End":
               pygame.draw.rect(screen, "Green" , (x, y, CELL_SIZE, CELL_SIZE))

def handle_mouse(grid, item_being_held):
   if item_being_held == None:
      user_draw(grid)
   else:
      drag_flag(item_being_held)
   
def user_draw(grid):
   x,y = pygame.mouse.get_pos()
   cell_being_clicked = grid.get_cell_being_clicked((x,y))
   if cell.flag == None:                                  # We dont want to color the start or end flag
      switch_cell_and_filled_cell(cell_being_clicked)

def switch_cell_and_filled_cell(cell):
   if cell.is_filled:
      cell.color = DEFAULT_COLOR
      cell.is_filled = False
   else:
      cell.color = FILLED_CELL_COLOR
      cell.is_filled = True

def drag_flag(flag):
   grid.change_flag_position(flag, pygame.mouse.get_pos())


grid = Grid()
mouse_is_held = False
item_being_held = None

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #When M1 is clicked
         cell = grid.get_cell_being_clicked(pygame.mouse.get_pos())
         item_being_held = cell.flag
         mouse_is_held = True
        
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #When M1 is released
         mouse_is_held = False

      
   if mouse_is_held:
      handle_mouse(grid, item_being_held)
      

   screen.fill(BLACK)
   draw_grid(grid)

   pygame.display.update()
   clock.tick(60)
