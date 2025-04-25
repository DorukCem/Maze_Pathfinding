from settings import *
from collections import deque
import pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
start_flag_surface = pygame.image.load("assests/start_flag.png")
start_flag_surface = pygame.transform.scale(start_flag_surface, IMAGE_SIZE)
end_flag_surface = pygame.image.load("assests/end_flag.png")
end_flag_surface = pygame.transform.scale(end_flag_surface, IMAGE_SIZE)
