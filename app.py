import os
import threading
import pygame

from alert import AlertManager
from file_count import FileCountHandler
from grid import Grid
from manager import Manager
from settings import *
from watchdog.observers import Observer
from utility import *


class App:
    def __init__(self):
        self.init_app()

        # These are used mainly by pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", TEXT_SIZE)
        self.alert_font = pygame.font.SysFont("Arial", ALERT_TEXT_SIZE)

        self.algorithm_manager = Manager()
        self.grid = Grid()

        # States which the app can hold
        self.mouse_is_held = False
        self.flag_held = None
        self.grid_needs_reset = False
        self.current_thread: threading.Thread | None = None # Algorithms are run ona seperate thread so that the app can is still interactive
        self.show_start_screen = True
        self.alerts = AlertManager()
        self.saved_file_count = 0 

        # Monitor number of files in saved_grids
        # (We go to the toruble of watching the directory so that external events can also be handled)
        self.event_handler = FileCountHandler("saved_grids")
        self.observer = Observer()
        self.init_file_observer()

    def init_app(self):
        os.makedirs("saved_grids", exist_ok=True)
        pygame.init()
        pygame.font.init()

    def init_file_observer(self):
        self.observer.schedule(self.event_handler, path="saved_grids", recursive=False)
        self.observer.start()

    def handle_mouse(self):
        x, y = pygame.mouse.get_pos()
        # If mouse is out of screen we do not want to handle it
        if x <= 0 or x >= WIDTH - 1 or y <= 0 or y >= HEIGHT - 1:
            return

        if self.flag_held == None:
            self.user_draw((x, y))
        else:
            self.drag_flag(self.flag_held, (x, y))

    def user_draw(self, mouse_pos):
        x, y = mouse_pos
        cell_being_clicked = self.grid.get_cell_being_clicked((x, y))
        if (
            cell_being_clicked.flag == None
        ):  # We dont want to color the start or end flag
            self.switch_cell_and_filled_cell(cell_being_clicked)

    def switch_cell_and_filled_cell(self, cell):
        if cell is self.grid.cell_that_switched_last:
            # To stop flickering when pressing a cell
            return
        else:
            self.grid.cell_that_switched_last = cell

        if cell.is_filled:
            cell.color = DEFAULT_COLOR
            cell.is_filled = False
        else:
            cell.color = FILLED_CELL_COLOR
            cell.is_filled = True

    def drag_flag(self, flag, mouse_pos):
        self.grid.change_flag_position(flag, mouse_pos)

    def scroll(self, direction):
        self.algorithm_manager.scroll(direction)

    def draw_algorithm_text(self, font: pygame.font.Font):
        text = self.algorithm_manager.get_selected_algorithm()
        text_surface = font.render(text, True, TEXT_COLOR)
        text_surface.set_alpha(170)
        self.screen.blit(text_surface, (10, 10))

    def draw_start_screen(self):
        self.screen.fill(DARK_BG)

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
            self.screen.blit(surf, (x, y))
            y += surf.get_height() + 20

    def draw_num_files_saved(self, saved_file_count, font: pygame.font.Font):
        x = 10
        y = HEIGHT - font.get_height()
        text_surface = font.render(f"NUM SAVES: {saved_file_count}", True, TEXT_COLOR)
        text_surface.set_alpha(170)
        self.screen.blit(text_surface, (x, y))

    def run_algorithm(self):
        self.algorithm_manager.run_algorithm(self.grid)

    def get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if self.show_start_screen:
                    self.show_start_screen = False
                    continue

            # Only process these inputs if no algorithm is running
            if self.current_thread is None:
                # --- Mouse Inputs ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        cell = self.grid.get_cell_being_clicked(pygame.mouse.get_pos())
                        self.flag_held = cell.flag
                        self.mouse_is_held = True

                        if self.grid_needs_reset:
                            self.grid.reset_grid()
                            self.grid_needs_reset = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.grid.cell_that_switched_last = None
                    self.mouse_is_held = False

                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll("up" if event.y == 1 else "down")

                # --- Keyboard Inputs ---
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        th = threading.Thread(target=lambda: self.run_algorithm())
                        th.start()
                        self.current_thread = th
                        self.grid_needs_reset = True

                    elif event.key == pygame.K_s:
                        save_grid(self.grid, self.alerts)

                    elif event.key == pygame.K_c:
                        self.grid.reset_grid()
                        self.grid_needs_reset = False

                    elif event.key == pygame.K_d:
                        delete_saves(self.alerts)

                    elif event.key == pygame.K_UP:
                        self.scroll("up")

                    elif event.key == pygame.K_DOWN:
                        self.scroll("down")

                    elif pygame.K_0 <= event.key <= pygame.K_9:
                        number_pressed = event.key - pygame.K_0
                        self.grid = load_grid(number_pressed, self.alerts) or self.grid

                    elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                        number_pressed = event.key - pygame.K_KP0
                        self.grid = load_grid(number_pressed, self.alerts) or self.grid
            else:
                # Stop algorithm
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.grid.kill_thread = True
                    self.grid.reset_grid()

    def main_loop(self):
        while True:
            if self.current_thread is not None and not self.current_thread.is_alive():
                self.current_thread = None

            self.get_user_input()

            if self.show_start_screen:
                self.draw_start_screen()

            else:
                if self.mouse_is_held:
                    self.handle_mouse()
                self.alerts.filter_alerts()

                self.screen.fill(BLACK)
                self.grid.draw(self.screen)
                self.draw_algorithm_text(self.font)
                self.draw_num_files_saved(self.saved_file_count, self.alert_font)
                self.alerts.draw_alerts(self.screen, self.alert_font)

                self.saved_file_count = self.event_handler.get_file_count()

            pygame.display.update()
            self.clock.tick(60)
