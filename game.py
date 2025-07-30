from board import Board
from piece import Piece
import pygame
from constants import *
from constants import BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS
import random 




class Game:
    def __init__(self):
        self.board = Board(BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)
        self.current_piece = self.new_piece()
        self.drop_timer = 0
        self.drop_interval = 500
        self.game_over = False

    def new_piece(self):
        return Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)

    def update(self, dt):
        if self.game_over:
            return
        self.drop_timer += dt
        if self.drop_timer > self.drop_interval:
            self.drop_timer = 0
            self.move_piece(0, 1)

    def move_piece(self, dx, dy):
        self.current_piece.move(dx, dy)
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.undo_move(dx, dy)
            if dy != 0:
                self.board.lock_piece(self.current_piece)
                self.board.clear_lines()
                self.current_piece = self.new_piece()
                if not self.board.is_valid_position(self.current_piece):
                    self.game_over = True

    def rotate_piece(self):
        self.current_piece.rotate()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.undo_rotate()

    def draw(self, screen):
        self.board.draw(screen)
        for x, y in self.current_piece.get_blocks():
            rect = pygame.Rect(PLAY_AREA_X + x * GRID_SIZE, PLAY_AREA_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.current_piece.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
