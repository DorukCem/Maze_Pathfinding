import pygame

from grid import Grid
from manager import Manager
from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", TEXT_SIZE)
        self.alert_font = pygame.font.SysFont("Arial", ALERT_TEXT_SIZE)
        self.manager = Manager()
        self.grid = Grid()

    def handle_mouse(self, item_being_held):
        x, y = pygame.mouse.get_pos()
        # If mouse is out of screen we get mouse pos that is equal to 0 or WIDTH-1 or HEIGHT-1
        if x <= 0 or x >= WIDTH - 1 or y <= 0 or y >= HEIGHT - 1:
            return

        if item_being_held == None:
            self.user_draw((x, y))
        else:
            self.drag_flag(item_being_held, (x, y))

    def user_draw(self, mouse_pos):
        x, y = mouse_pos
        cell_being_clicked = self.grid.get_cell_being_clicked((x, y))
        if (
            cell_being_clicked.flag == None
        ):  # We dont want to color the start or end flag
            self.switch_cell_and_filled_cell(cell_being_clicked)

    def switch_cell_and_filled_cell(self, cell):
        if cell is self.grid.cell_that_switched_last:
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
        self.manager.scroll(direction)

    def draw_algorithm_text(self, font: pygame.font.Font):
        text = self.manager.get_selected_algorithm()
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
        self.manager.run_algorithm(self.grid)
