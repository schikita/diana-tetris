import pygame
import random

from constants import *

class Piece:
    def __init__(self, shape_index, board_width_block, board_height_blocks):
        self.shape_index = shape_index
        self.shape_data = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.rotation = 0
        self.x = board_width_block // 2 - 2
        self.y = 0

    def get_blocks(self):
        return [(self.x + c, self.y + r) for r, c in self.shape_data[self.rotation]]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_data)

    def undo_rotate(self):
        self.rotation = (self.rotation - 1) % len(self.shape_data)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def undo_move(self, dx, dy):
        self.x -= dx
        self.y -= dy