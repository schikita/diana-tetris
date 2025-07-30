import pygame
from game import Game
from constants import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    dt = clock.tick(60)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT:
                game.move_piece(1, 0)
            elif event.key == pygame.K_DOWN:
                game.move_piece(0, 1)
            elif event.key == pygame.K_UP:
                game.rotate_piece()

    game.update(dt)
    game.draw(screen)
    pygame.display.flip()

pygame.quit()
