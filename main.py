import os
from sys import exit
import threading
from grid import Grid
from manager import Manager

from settings import *
from collections import deque
import pygame
import pickle

os.makedirs("saved_grids", exist_ok=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Arial", TEXT_SIZE)

pygame.init()


def handle_mouse(grid, item_being_held):
    if item_being_held == None:
        user_draw(grid)
    else:
        drag_flag(item_being_held)


def user_draw(grid):
    x, y = pygame.mouse.get_pos()
    cell_being_clicked = grid.get_cell_being_clicked((x, y))
    if cell_being_clicked.flag == None:  # We dont want to color the start or end flag
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


def draw_text(font: pygame.font.Font):
    text = manager.get_selected_algorithm()
    text_surface = font.render(text, True, TEXT_COLOR)
    text_surface.set_alpha(170)
    screen.blit(text_surface, (10, 10))


def save_grid(grid: Grid):
    try:
        for i in range(10):
            filepath = os.path.join("saved_grids", str(i))
            if os.path.exists(filepath):
                continue

            with open(filepath, mode="wb") as file:
                pickle.dump(grid, file)
                print(f"Saved grid with id: {i}")
                return

    except Exception as e:
        print(f"Could not save because: {e}")

    print("Could not save becase. Can have at most 10 grids saved.")


def load_grid(grid: Grid, id: int) -> Grid:
    """
    WARNING: This function mutates grid if can find the saved file
    """
    path = os.path.join("saved_grids", str(id))
    try:
        if not os.path.exists(path):
            print(f"Saved grid with id:{id} does not exits ")
            return

        with open(path, "rb") as infile:
            new_grid = pickle.load(infile)
            print(f"Loaded grid with id {id}")
            return new_grid

    except Exception as e:
        print(f"Could not load because: {e}")


grid = Grid()
manager = Manager()
mouse_is_held = False
item_being_held = None
grid_needs_reset = False
current_th: threading.Thread | None = None

while True:
    if current_th != None:
        if not current_th.is_alive():
            current_th = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if current_th == None:
            if (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):  # When M1 is clicked
                cell = grid.get_cell_being_clicked(pygame.mouse.get_pos())
                item_being_held = cell.flag
                mouse_is_held = True

            if (
                event.type == pygame.MOUSEBUTTONUP and event.button == 1
            ):  # When M1 is released
                grid.cell_that_switched_last = None
                mouse_is_held = False

            if event.type == pygame.MOUSEWHEEL:  # On scroll
                if event.y == 1:
                    scroll(manager, "up")
                else:
                    scroll(manager, "down")

            if event.type == pygame.KEYDOWN or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                if grid_needs_reset:
                    grid.reset_grid()
                    grid_needs_reset = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                th = threading.Thread(target=lambda: manager.run_algorithm(grid))
                th.start()
                current_th = th
                grid_needs_reset = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                save_grid(grid)

            if event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    number_pressed = event.key - pygame.K_0
                    grid = load_grid(grid, number_pressed) or grid
                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    number_pressed = event.key - pygame.K_KP0
                    grid = load_grid(grid, number_pressed) or grid

    if mouse_is_held:
        handle_mouse(grid, item_being_held)

    screen.fill(BLACK)
    grid.draw(screen)
    draw_text(font)

    pygame.display.update()
    clock.tick(60)
