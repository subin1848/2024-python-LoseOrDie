import pygame
from src.settings import WHITE, BLACK, FONT_PATH_TITLE, FONT_PATH_BODY, FONT_SIZE_TITLE, FONT_SIZE_BODY, WIDTH, HEIGHT

def show_popup(screen, round_info, clock):
    # Round 1 텍스트 표시
    font = pygame.font.Font(FONT_PATH_BODY, 36)
    round_text = font.render(f"Round {round_info['round']} 시작!", True, WHITE)

    timer = 0
    while timer < 120:  # 2초 동안 Round 1 텍스트 표시
        screen.fill((0, 0, 0))
        screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, HEIGHT // 2 - round_text.get_height() // 2))
        pygame.display.flip()
        timer += 1
        clock.tick(60)

    # 팝업창 표시
    popup_running = True
    popup_bg = pygame.Surface((600, 400))
    popup_bg.fill((255, 255, 200))

    title_font = pygame.font.Font(FONT_PATH_TITLE, FONT_SIZE_TITLE)
    body_font = pygame.font.Font(FONT_PATH_BODY, FONT_SIZE_BODY)

    title_text = title_font.render(f"Round {round_info['round']}", True, BLACK)
    required_food_text = body_font.render(f"먹어야 되 : {', '.join([food['name'] for food in round_info['required_food']])}", True, BLACK)
    avoid_food_text = body_font.render(f"먹으면 안되 : {', '.join([food['name'] for food in round_info['avoid_food']])}", True, BLACK)
    start_text = body_font.render("SPACE 키를 눌러 게임을 시작하세요", True, BLACK)

    while popup_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                popup_running = False

        screen.blit(popup_bg, ((WIDTH - 600) // 2, (HEIGHT - 400) // 2))
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, (HEIGHT - 400) // 2 + 50))
        screen.blit(required_food_text, ((WIDTH - required_food_text.get_width()) // 2, (HEIGHT - 400) // 2 + 150))
        screen.blit(avoid_food_text, ((WIDTH - avoid_food_text.get_width()) // 2, (HEIGHT - 400) // 2 + 200))
        screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - 400) // 2 + 300))

        pygame.display.flip()
        clock.tick(60)