import pygame
from constants import *

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def is_valid_position(self, piece, adj_x=0, adj_y=0):
        for x, y in piece.get_blocks():
            x += adj_x
            y += adj_y
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            if self.grid[y][x] is not None:
                return False
        return True

    def lock_piece(self, piece):
        for x, y in piece.get_blocks():
            self.grid[y][x] = piece.color


    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                color = self.grid[y][x]
                if color:
                    rect = pygame.Rect(PLAY_AREA_X + x * GRID_SIZE, PLAY_AREA_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.height - len(new_grid)
        while len(new_grid) < self.height:
            new_grid.insert(0, [None for _ in range(self.width)])
        self.grid = new_grid
        return cleared
