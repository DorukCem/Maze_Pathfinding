import os
from sys import exit
import shutil
import threading
from typing import List
from grid import Grid
from manager import Manager

from settings import *
from collections import deque
import pygame
import pickle
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

os.makedirs("saved_grids", exist_ok=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Arial", TEXT_SIZE)
alert_font = pygame.font.SysFont("Arial", ALERT_TEXT_SIZE)

pygame.init()

# TODO add command line arg for scale

def handle_mouse(grid, item_being_held):
    x, y = pygame.mouse.get_pos()
    # If mouse is out of screen we get mouse pos that is equal to 0 or WIDTH-1 or HEIGHT-1
    if x <= 0 or x >= WIDTH - 1 or y <= 0 or y >= HEIGHT - 1:
        return

    if item_being_held == None:
        user_draw(grid, (x, y))
    else:
        drag_flag(item_being_held, (x, y))


def user_draw(grid, mouse_pos):
    x, y = mouse_pos
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


def drag_flag(flag, mouse_pos):
    grid.change_flag_position(flag, mouse_pos)


def scroll(manager, direction):
    manager.scroll(direction)


def draw_algorithm_text(font: pygame.font.Font):
    text = manager.get_selected_algorithm()
    text_surface = font.render(text, True, TEXT_COLOR)
    text_surface.set_alpha(170)
    screen.blit(text_surface, (10, 10))


class Alert:
    def __init__(self, text, duration=ALERT_DURATION):
        self.text = text
        self.duration = duration

    def draw_alert(self, y_pos, font: pygame.font.Font):
        text_surface = font.render(self.text, True, ALERT_TEXT_COLOR)
        w = text_surface.get_width()
        text_surface.set_alpha(170)
        screen.blit(text_surface, (WIDTH - w - 20, 10 + y_pos))


class AlertManager:
    def __init__(self):
        self.alerts: List[Alert] = []

    def append_from_str(self, txt: str):
        print(
            txt
        )  # I think logging this to the console can be good to see alerts after they have expired
        self.alerts.append(Alert(txt))

    def filter_alerts(self):
        self.alerts = [a for a in self.alerts if a.duration > 0]

    def draw_alerts(self, font: pygame.font.Font):
        y_pos = 0
        for a in self.alerts:
            a.duration -= 1
            a.draw_alert(y_pos, font)
            y_pos += font.get_height() + 10


class FileCountHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.file_count = self.get_file_count()

    def get_file_count(self):
        # Count only files (not directories)
        return len(
            [
                f
                for f in os.listdir(self.directory)
                if os.path.isfile(os.path.join(self.directory, f))
            ]
        )

    def on_created(self, event):
        if not event.is_directory:
            self.file_count += 1

    def on_deleted(self, event):
        if not event.is_directory:
            self.file_count -= 1


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


def draw_start_screen():
    screen.fill(DARK_BG)

    # Use smaller font for instructions
    start_font = pygame.font.SysFont(FONT, START_SCREEN_TEXT_SIZE)
    header_font = pygame.font.SysFont(FONT, START_SCREEN_HEADER_SIZE, bold=True)

    # Instructions text
    README_TEXT = [
        "Controls:",
        "- Drag start/end flags with your mouse",
        "- Draw/delete walls with the mouse",
        "- Scroll or use UP/DOWN arrow keys to switch algorithms",
        "- Press SPACE to start/stop the algorithm",
        "- Press C to clear trails or draw to clear",
        "- Press S to save the grid (ID 0-9)",
        "- Press 0-9 to load a saved grid",
        "- You can have at most 10 saves",
        "- Press D to delete all saved grids",
        "",
        "Press SPACE to start...",
    ]

    # Calculate total height for centering
    total_height = 0
    rendered_lines = []
    for i, line in enumerate(README_TEXT):
        font = header_font if i == 0 else start_font
        surf = font.render(line, True, WHITE)
        rendered_lines.append((surf, font))
        total_height += surf.get_height() + 20

    start_y = (HEIGHT - total_height) // 2

    # Blit each line centered
    y = start_y
    for surf, font in rendered_lines:
        x = (WIDTH - surf.get_width()) // 2
        screen.blit(surf, (x, y))
        y += surf.get_height() + 20


def draw_num_files_saved(saved_file_count, font: pygame.font.Font):
    x = 10
    y = HEIGHT - font.get_height()
    text_surface = font.render(f"NUM SAVES: {saved_file_count}", True, TEXT_COLOR)
    text_surface.set_alpha(170)
    screen.blit(text_surface, (x, y))


grid = Grid()
manager = Manager()
mouse_is_held = False
item_being_held = None
grid_needs_reset = False
current_thread: threading.Thread | None = None
is_start_screen = True
alerts = AlertManager()

# Monitor number of files is saved_grids
# (We go to the toruble of watching the directory so that external events can also be handled)
event_handler = FileCountHandler("saved_grids")
observer = Observer()
observer.schedule(event_handler, path="saved_grids", recursive=False)
observer.start()

while True:
    if current_thread is not None and not current_thread.is_alive():
        current_thread = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if is_start_screen:
                is_start_screen = False
                continue

        # Only process inputs if no algorithm is running
        if current_thread is None:
            # --- Mouse Inputs ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    cell = grid.get_cell_being_clicked(pygame.mouse.get_pos())
                    item_being_held = cell.flag
                    mouse_is_held = True

                    if grid_needs_reset:
                        grid.reset_grid()
                        grid_needs_reset = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                grid.cell_that_switched_last = None
                mouse_is_held = False

            elif event.type == pygame.MOUSEWHEEL:
                scroll(manager, "up" if event.y == 1 else "down")

            # --- Keyboard Inputs ---
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    th = threading.Thread(target=lambda: manager.run_algorithm(grid))
                    th.start()
                    current_thread = th
                    grid_needs_reset = True

                elif event.key == pygame.K_s:
                    save_grid(grid, alerts)

                elif event.key == pygame.K_c:
                    grid.reset_grid()
                    grid_needs_reset = False

                elif event.key == pygame.K_d:
                    delete_saves(alerts)

                elif event.key == pygame.K_UP:
                    scroll(manager, "up")

                elif event.key == pygame.K_DOWN:
                    scroll(manager, "down")

                elif pygame.K_0 <= event.key <= pygame.K_9:
                    number_pressed = event.key - pygame.K_0
                    grid = load_grid(number_pressed, alerts) or grid

                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    number_pressed = event.key - pygame.K_KP0
                    grid = load_grid(number_pressed, alerts) or grid
        else:
            # Stop algorithm
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Grid is accesed by the algorithm that is executed which will check on each iteration if this is true
                grid.kill_thread = True
                grid.reset_grid()

    if is_start_screen:
        draw_start_screen()

    else:
        if mouse_is_held:
            handle_mouse(grid, item_being_held)

        screen.fill(BLACK)
        grid.draw(screen)
        draw_algorithm_text(font)

        alerts.filter_alerts()
        alerts.draw_alerts(alert_font)

        saved_file_count = event_handler.get_file_count()
        draw_num_files_saved(saved_file_count, alert_font)

    pygame.display.update()
    clock.tick(60)
