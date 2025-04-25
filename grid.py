from cell import Cell
from settings import *
import pygame

start_flag_surface = pygame.image.load("assests/start_flag.png")
start_flag_surface = pygame.transform.scale(start_flag_surface, IMAGE_SIZE)
end_flag_surface = pygame.image.load("assests/end_flag.png")
end_flag_surface = pygame.transform.scale(end_flag_surface, IMAGE_SIZE)


class Grid:
    def __init__(self):
        self.width = WIDTH
        self.height = WIDTH
        self.array = [
            [Cell(i, j) for i in range(0, WIDTH, CELL_SIZE)]
            for j in range(0, HEIGHT, CELL_SIZE)
        ]

        self.start_flag_cell = None
        self.end_flag_cell = None
        self.setup_flags()

        self.cell_that_switched_last = None  # So that cells do not flicker

    def setup_flags(self):
        x = int(GRIDWITH / 2)
        y = int(GRIDHEIGHT / 2)
        self.array[y][x].flag = "Start"
        self.array[y][x + 1].flag = "End"
        self.start_flag_cell = self.array[y][x]
        self.end_flag_cell = self.array[y][x + 1]

    def reset_grid(self):
        for row in self.array:
            for cell in row:
                if cell.is_filled == False:
                    cell.color = DEFAULT_COLOR
                cell.prev = None
                cell.distance_from_end = None
                cell.distance_from_start = None

    def get_cell_being_clicked(self, coordinate):
        x, y = coordinate
        cell_index_x = x // CELL_SIZE
        cell_index_y = y // CELL_SIZE
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

    def draw(self, screen):
        for row in self.array:
            for cell in row:
                x, y = cell.x, cell.y
                pygame.draw.rect(screen, cell.color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(
                    screen, cell.border_color, (x, y, CELL_SIZE, CELL_SIZE), 1
                )
                if cell.flag == "Start":
                    screen.blit(start_flag_surface, (x, y))
                if cell.flag == "End":
                    screen.blit(end_flag_surface, (x, y))
