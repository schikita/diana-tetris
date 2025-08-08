import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

def run_intro(screen, clock, duration_ms=1800):
    title_font = pygame.font.SysFont("arial", 64, bold=True)
    small_font = pygame.font.SysFont("arial", 24)
    start = pygame.time.get_ticks()

    while True:
        dt = clock.tick(60)
        t = pygame.time.get_ticks() - start
        alpha = min(255, int(255 * (t / 600)))  # fade-in первые ~0.6с

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                return "skip"

        screen.fill(BLACK)
        title = title_font.render("TETRIS", True, WHITE)
        by = small_font.render("Press any key to continue", True, WHITE)

        title.set_alpha(alpha)
        by.set_alpha(alpha)

        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 80))
        screen.blit(by, (SCREEN_WIDTH//2 - by.get_width()//2, SCREEN_HEIGHT//2 + 10))
        pygame.display.flip()

        if t >= duration_ms:
            return "done"
