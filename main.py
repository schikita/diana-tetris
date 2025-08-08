import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAY, UI_COLOR, UI_ACCENT, PLAY_AREA_X, PLAY_AREA_Y
from game import Game
from state import GameState
from ui import Menu
from records import top_records, save_record
from settings import Settings
from intro import run_intro

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 48, bold=True)
font_mid = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)

settings = Settings()
game = Game(settings)
game.set_volumes_from_settings()

state = GameState.INTRO

def draw_center_text(lines, y0):
    for i, (txt, fnt, color) in enumerate(lines):
        surf = fnt.render(txt, True, color)
        screen.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, y0 + i*50))

def show_menu():
    items = [
        ("Start Game", "start"),
        ("Records", "records"),
        ("Settings", "settings"),
        ("Quit", "quit"),
    ]
    return Menu(font_mid, items)

menu = show_menu()
paused_menu = Menu(font_mid, [("Resume", "resume"), ("Main Menu", "menu"), ("Quit", "quit")])

running = True
player_name_input = ""
input_active = False

while running:
    dt = clock.tick(60)
    screen.fill(GRAY)

    # INTRO
    if state == GameState.INTRO:
        r = run_intro(screen, clock)
        if r == "quit":
            break
        state = GameState.MENU
        continue

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU navigation
        if state == GameState.MENU:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    menu.move(-1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    menu.move(1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tag = menu.current()
                    if tag == "start":
                        game = Game(settings)
                        game.set_volumes_from_settings()
                        state = GameState.GAME
                    elif tag == "records":
                        state = GameState.RECORDS
                    elif tag == "settings":
                        state = GameState.SETTINGS
                    elif tag == "quit":
                        running = False

        elif state == GameState.GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = GameState.PAUSE
                elif event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

        elif state == GameState.PAUSE:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    paused_menu.move(-1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    paused_menu.move(1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tag = paused_menu.current()
                    if tag == "resume":
                        state = GameState.GAME
                    elif tag == "menu":
                        state = GameState.MENU
                    elif tag == "quit":
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    state = GameState.GAME

        elif state == GameState.SETTINGS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = GameState.MENU
                elif event.key == pygame.K_LEFT:
                    settings.music_volume -= 0.05
                elif event.key == pygame.K_RIGHT:
                    settings.music_volume += 0.05
                elif event.key == pygame.K_UP:
                    settings.sfx_volume += 0.05
                elif event.key == pygame.K_DOWN:
                    settings.sfx_volume -= 0.05
                elif event.key == pygame.K_a:
                    settings.brightness -= 0.05
                elif event.key == pygame.K_d:
                    settings.brightness += 0.05
                settings.clamp()
                game.set_volumes_from_settings()

        elif state == GameState.RECORDS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = GameState.MENU

        elif state == GameState.GAME_OVER:
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    save_record(player_name_input or "Player", game.score)
                    input_active = False
                    state = GameState.MENU
                elif event.key == pygame.K_BACKSPACE:
                    player_name_input = player_name_input[:-1]
                else:
                    if len(player_name_input) < 16 and event.unicode.isprintable():
                        player_name_input += event.unicode

    # DRAW / UPDATE by state
    if state == GameState.MENU:
        draw_center_text([("TETRIS", font_big, UI_ACCENT)], 120)
        menu.draw(screen, SCREEN_WIDTH//2 - 120, 260)
    elif state == GameState.GAME:
        game.update(dt)
        game.draw(screen, font_small, font_big)
        if game.game_over:
            player_name_input = ""
            input_active = True
            state = GameState.GAME_OVER
    elif state == GameState.PAUSE:
        game.draw(screen, font_small, font_big)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,170))
        screen.blit(overlay, (0,0))
        draw_center_text([("PAUSED", font_big, UI_ACCENT)], 160)
        paused_menu.draw(screen, SCREEN_WIDTH//2 - 120, 260)
    elif state == GameState.SETTINGS:
        lines = [
            ("SETTINGS", font_big, UI_ACCENT),
            (f"Music Volume  [Left/Right]: {settings.music_volume:.2f}", font_small, UI_COLOR),
            (f"SFX Volume    [Up/Down]   : {settings.sfx_volume:.2f}", font_small, UI_COLOR),
            (f"Brightness    [A / D]     : {settings.brightness:.2f}", font_small, UI_COLOR),
            ("Esc - Back", font_small, UI_COLOR),
        ]
        draw_center_text(lines, 120)
    elif state == GameState.RECORDS:
        records = top_records()
        draw_center_text([("RECORDS", font_big, UI_ACCENT)], 80)
        y = 170
        for i, r in enumerate(records or []):
            txt = f"{i+1:2d}. {r['name']:<16}  {r['score']}"
            surf = font_small.render(txt, True, UI_COLOR)
            screen.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, y))
            y += 34
        if not records:
            draw_center_text([("No records yet", font_small, UI_COLOR)], 200)
        draw_center_text([("Esc - Back", font_small, UI_COLOR)], SCREEN_HEIGHT-100)
    elif state == GameState.GAME_OVER:
        game.draw(screen, font_small, font_big)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        screen.blit(overlay, (0,0))
        draw_center_text([
            ("GAME OVER", font_big, UI_ACCENT),
            (f"Your score: {game.score}", font_mid, UI_COLOR),
            ("Enter your name and press Enter:", font_small, UI_COLOR),
        ], 140)
        box = pygame.Rect(SCREEN_WIDTH//2 - 180, 280, 360, 44)
        pygame.draw.rect(screen, (30,30,30), box)
        pygame.draw.rect(screen, UI_ACCENT, box, 2)
        name_surf = font_small.render(player_name_input or "_", True, UI_COLOR)
        screen.blit(name_surf, (box.x + 10, box.y + 10))

    pygame.display.flip()

pygame.quit()
