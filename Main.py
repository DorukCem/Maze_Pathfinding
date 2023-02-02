from sys import exit
from global_objects import*
from grid import Grid
from manager import Manager

pygame.font.init()
font = pygame.font.SysFont("Arial", TEXT_SIZE)

pygame.init() 

def handle_mouse(grid, item_being_held):
   if item_being_held == None:
      user_draw(grid)
   else:
      drag_flag(item_being_held)
   
def user_draw(grid):
   x,y = pygame.mouse.get_pos()
   cell_being_clicked = grid.get_cell_being_clicked((x,y))
   if cell_being_clicked.flag == None:                                  # We dont want to color the start or end flag
      switch_cell_and_filled_cell(cell_being_clicked)

def switch_cell_and_filled_cell(cell):        
   if cell is grid.cell_that_switched_last:
      return
   else:
      grid.cell_that_switched_last = cell
   
   if cell.is_filled:
      cell.color = DEFAULT_COLOR
      cell.is_filled = False
   else:
      cell.color = FILLED_CELL_COLOR
      cell.is_filled = True

def drag_flag(flag):
   grid.change_flag_position(flag, pygame.mouse.get_pos())

def scroll(manager, direction):
   manager.scroll(direction)
   
   
def draw_text(font):
   text = manager.get_selected_algorithm()
   text_surface = font.render(text, True, TEXT_COLOR)
   screen.blit(text_surface, (10, 10))


grid = Grid()
manager = Manager()
mouse_is_held = False
item_being_held = None
grid_needs_reset = False
text_timer = 0           #In order to show text a few seconds after scrolling


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
         grid.cell_that_switched_last = None
         mouse_is_held = False

      if event.type ==  pygame.MOUSEWHEEL: #On scroll
         text_timer = TEXT_TIME
         if event.y == 1:
            scroll(manager, "up")
         else:
            scroll(manager, "down")
      
      if event.type == pygame .KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
         if grid_needs_reset:
            grid.reset_grid()
            grid_needs_reset = False
         
      if event.type == pygame .KEYDOWN and event.key == pygame.K_SPACE:
         manager.run_algorithm(grid)
         grid_needs_reset = True

   if mouse_is_held:
      handle_mouse(grid, item_being_held)
   

   screen.fill(BLACK)
   grid.draw()
   if text_timer:
      draw_text(font)
      text_timer -= 1

   pygame.display.update()
   clock.tick(60)
