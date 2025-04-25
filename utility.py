from settings import *


def draw_final_path(grid):
    if grid.end_flag_cell.prev:
        cell = grid.end_flag_cell
        while cell.prev:
            cell.color = FINAL_PATH_COLOR
            cell = cell.prev

        grid.start_flag_cell.color = FINAL_PATH_COLOR


def check_out_of_bounds(grid, i, j):
    if (
        i < 0 or j < 0 or i >= len(grid.array) or j >= len(grid.array[0])
    ):  # Check out of bounds
        return False
    else:
        return True
