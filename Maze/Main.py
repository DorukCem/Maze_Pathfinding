import pygame
from sys import exit
from settings import *
from grid import Grid
 

pygame.init()
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()

def draw(grid):
   for row in grid.array:
         for cell in row:
            x,y = cell.x, cell.y
            pygame.draw.rect(screen, cell.color , (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, cell.border_color, (x, y, CELL_SIZE, CELL_SIZE), 1)


def handle_mouse(grid, click_mode):
   if click_mode == 1:
      draw_cells(grid)
   if click_mode == 2:
      pass

def draw_cells(grid):
   x,y = pygame.mouse.get_pos()
   cell_being_clicked = grid.get_cell_being_clicked((x,y))
   cell_being_clicked.color = "Black"

grid = Grid()
mouse_is_held = False
click_mode = None

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #When M1 is clicked
         mouse_is_held = True
         click_mode = 1 

      if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #When M1 is released
         click_mode = None
         mouse_is_held = False

      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2: #When M2 is clicked
         cell_being_clicked = grid.get_cell_being_clicked(pygame.mouse.get_pos())
         if cell_being_clicked.property in ["Start", "End"]:
            click_mode = 2
         mouse_is_held = True
         
      if event.type == pygame.MOUSEBUTTONUP and event.button == 2: #When M2 is released
         click_mode = None
         mouse_is_held = False

   
   if mouse_is_held:
      handle_mouse(grid)

   screen.fill(BLACK)
   draw(grid)

   pygame.display.update()
   clock.tick(60)
