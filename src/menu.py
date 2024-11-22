import pygame
from src.settings import FONT_PATH_TITLE, FONT_PATH_BODY, FONT_SIZE_TITLE, FONT_SIZE_BODY, WHITE, BLACK

def main_menu(screen, background_img, clock):
    # 폰트 로드 및 텍스트 생성
    blink_font = pygame.font.Font(FONT_PATH_BODY, FONT_SIZE_BODY)

    blink_text = blink_font.render("Press ENTER to Begin", True, WHITE)

    # 텍스트 위치 중앙 조정
    blink_rect = blink_text.get_rect(center=(screen.get_width() // 2, 300))

    blink = True
    blink_timer = 0
    running = True

    while running:
        # 배경 렌더링
        screen.blit(background_img, (0, 0))

        # 깜빡이는 텍스트 렌더링
        blink_timer += 1
        if blink_timer % 30 == 0:
            blink = not blink
        if blink:
            screen.blit(blink_text, blink_rect)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        pygame.display.flip()
        clock.tick(60)
