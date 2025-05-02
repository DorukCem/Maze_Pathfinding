import os
import pickle
import shutil
from alert import AlertManager
from grid import Grid
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

def save_grid(grid: Grid, alerts: AlertManager):
    try:
        for i in range(10):
            filepath = os.path.join("saved_grids", str(i))
            if os.path.exists(filepath):
                continue

            with open(filepath, mode="wb") as file:
                pickle.dump(grid, file)
                alerts.append_from_str(f"Saved grid with id: {i}")
                return

    except Exception as e:
        alerts.append_from_str(f"Could not save because: {e}")

    alerts.append_from_str("Could not save becase. Can have at most 10 grids saved.")


def load_grid(id: int, alerts: AlertManager) -> Grid:
    """
    WARNING: This function mutates grid if can find the saved file
    """
    path = os.path.join("saved_grids", str(id))
    try:
        if not os.path.exists(path):
            alerts.append_from_str(f"Saved grid with id:{id} does not exits ")
            return

        with open(path, "rb") as infile:
            new_grid = pickle.load(infile)
            alerts.append_from_str(f"Loaded grid with id: {id}")
            new_grid.reset_grid()
            return new_grid

    except Exception as e:
        alerts.append_from_str(f"Could not load because: {e}")


def delete_saves(alerts: AlertManager):
    folder = "saved_grids"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            alerts.append_from_str(f"Failed to delete {file_path}. Reason: {e}")
    alerts.append_from_str("Deleted all saves")

