import pygame

class Menu:
    def __init__(self, font, items):
        self.font = font
        self.items = items  # [(caption, tag)]
        self.index = 0

    def move(self, d):
        self.index = (self.index + d) % len(self.items)

    def current(self):
        return self.items[self.index][1]

    def draw(self, screen, x, y, spacing=50, color=(230,230,230), active=(255,215,0)):
        for i, (caption, _) in enumerate(self.items):
            surf = self.font.render(caption, True, active if i == self.index else color)
            screen.blit(surf, (x, y + i*spacing))
