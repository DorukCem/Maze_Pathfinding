from typing import List
import pygame
from settings import *


class Alert:
    def __init__(self, text, duration=ALERT_DURATION):
        self.text = text
        self.duration = duration

    def draw_alert(self, y_pos, screen, font: pygame.font.Font):
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

    def draw_alerts(self, screen, font: pygame.font.Font):
        y_pos = 0
        for a in self.alerts:
            a.duration -= 1
            a.draw_alert(y_pos, screen, font)
            y_pos += font.get_height() + 10
