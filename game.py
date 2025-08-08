from board import Board
from piece import Piece
import pygame, random
from constants import *
from pathlib import Path
from audio import resource_path, init_audio
from settings import Settings

init_audio()

SOUNDS_DIR = Path(resource_path("assets", "sounds"))

def safe_sound(path):
    try:
        s = pygame.mixer.Sound(str(path))
        return s
    except Exception:
        return None

BREAK_LINE_SOUND = safe_sound(SOUNDS_DIR / "break_line.mp3")
DOWN_SHAPE_SOUND = safe_sound(SOUNDS_DIR / "down_shape.mp3")
GAME_OVER_SOUND  = safe_sound(SOUNDS_DIR / "game_over.mp3")
SELECT_SOUND     = safe_sound(SOUNDS_DIR / "select.mp3")

try:
    pygame.mixer.music.load(str(SOUNDS_DIR / "music_game.mp3"))
except Exception:
    pass

class Game:
    def __init__(self, settings: Settings):
        self.settings = settings
        pygame.mixer.music.set_volume(self.settings.music_volume)
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

        self.board = Board(BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)
        self.current_piece = self.new_piece()
        self.drop_timer = 0
        self.drop_interval = 500
        self.game_over = False
        self._played_game_over = False

        # Очки
        self.score = 0

        # Яркость-оверлей
        self.brightness_surf = pygame.Surface((PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT), pygame.SRCALPHA)

    def set_volumes_from_settings(self):
        pygame.mixer.music.set_volume(self.settings.music_volume)
        for snd in (BREAK_LINE_SOUND, DOWN_SHAPE_SOUND, GAME_OVER_SOUND, SELECT_SOUND):
            if snd:
                snd.set_volume(self.settings.sfx_volume)

    def new_piece(self):
        return Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)

    def update(self, dt):
        if self.game_over:
            if not self._played_game_over:
                if GAME_OVER_SOUND: GAME_OVER_SOUND.play()
                try:
                    pygame.mixer.music.fadeout(800)
                except Exception:
                    pass
                self._played_game_over = True
            return

        self.drop_timer += dt
        if self.drop_timer > self.drop_interval:
            self.drop_timer = 0
            self.move_piece(0, 1)

    def add_score_for_lines(self, lines):
        if lines == 1: self.score += 100
        elif lines == 2: self.score += 300
        elif lines == 3: self.score += 500
        elif lines >= 4: self.score += 800

    def move_piece(self, dx, dy):
        self.current_piece.move(dx, dy)
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.undo_move(dx, dy)
            if dy != 0:  # посадка фигуры
                self.board.lock_piece(self.current_piece)
                cleared = self.board.clear_lines()
                if cleared and BREAK_LINE_SOUND: BREAK_LINE_SOUND.play()
                if DOWN_SHAPE_SOUND: DOWN_SHAPE_SOUND.play()
                self.add_score_for_lines(cleared)
                self.current_piece = self.new_piece()
                if not self.board.is_valid_position(self.current_piece):
                    self.game_over = True
        else:
            if dx != 0 and SELECT_SOUND: SELECT_SOUND.play()

    def rotate_piece(self):
        self.current_piece.rotate()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.undo_rotate()
        else:
            if SELECT_SOUND: SELECT_SOUND.play()

    def draw(self, screen, font_small, font_big):
        # поле
        self.board.draw(screen)
        for x, y in self.current_piece.get_blocks():
            rect = pygame.Rect(PLAY_AREA_X + x*GRID_SIZE, PLAY_AREA_Y + y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.current_piece.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

        # текущие очки
        score_surf = font_small.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_surf, (PLAY_AREA_X, PLAY_AREA_Y - 35))

        # яркость: затемняем/осветляем поверх области поля
        # для простоты: если brightness < 1 — кладём чёрный с альфой; если >1 — белый с альфой.
        if self.settings.brightness < 1.0:
            alpha = int(255 * (1.0 - self.settings.brightness) * 0.7)
            self.brightness_surf.fill((0,0,0,alpha))
            screen.blit(self.brightness_surf, (PLAY_AREA_X, PLAY_AREA_Y))
        elif self.settings.brightness > 1.0:
            alpha = int(255 * (self.settings.brightness - 1.0) * 0.6)
            self.brightness_surf.fill((255,255,255,alpha))
            screen.blit(self.brightness_surf, (PLAY_AREA_X, PLAY_AREA_Y))
