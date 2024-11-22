# 라운드 전환, 음식 충돌 감지, 게임 데이터 저장
import pygame, random
from .utils import save_to_json, load_json_data
from .settings import WIDTH, HEIGHT
from .food import spawn_food
from pygame.locals import *

# 게임 페이드 인/아웃 효과
def fade_in_out(screen, new_background):
    for alpha in range(0, 255, 5):  # 페이드 인
        screen.blit(new_background, (0, 0))
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(255 - alpha)
        fade_surface.fill((0, 0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

    pygame.time.delay(1000)  # 잠시 대기 후

    for alpha in range(255, 0, -5):  # 페이드 아웃
        screen.blit(new_background, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

# 게임 시작 메뉴에서 시작 버튼 클릭 대기
def main_menu(screen, background, clock):
    # 메뉴 화면 그리기
    screen.blit(background, (0, 0))

    # 시작 버튼 크기와 위치 설정 (예시로 화면 중앙에 버튼을 배치)
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # 시작 버튼 그리기 (예시로 단순한 사각형 버튼)
    pygame.draw.rect(screen, (0, 255, 0), start_button_rect)  # 녹색 버튼

    # 화면 업데이트
    pygame.display.flip()

    # 시작 버튼 클릭 대기
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 클릭
                    mouse_x, mouse_y = event.pos
                    # 시작 버튼 클릭 시
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        running = False  # 버튼 클릭 시 루프 종료
                        return  # 게임 루프 시작

        clock.tick(60)  # 프레임 속도 조절

# 라운드 전환, 음식 충돌 감지, 게임 데이터 저장
def handle_collisions(character, foods, game_data):
    good_food_eaten = False
    for food in foods[:]:
        if character.rect.colliderect(food.rect):
            if food.is_good_food:
                game_data["score"] += 1
                game_data["eaten_food_count"] += 1
                game_data["eaten_foods"].append(food.name)
                good_food_eaten = True
            else:
                game_data["lives"] -= 1
                game_data["combo_count"] = 0  # 나쁜 음식을 먹으면 콤보 리셋

            foods.remove(food)

    return game_data["lives"] > 0, good_food_eaten

def next_round(game_data, rounds, current_round, foods):
    if game_data["eaten_food_count"] >= 10:  # 음식 10개 먹으면 다음 라운드로
        current_round += 1
        foods.clear()
        game_data["eaten_food_count"] = 0
    return game_data, current_round
