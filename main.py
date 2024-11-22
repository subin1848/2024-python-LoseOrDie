import pygame
from src.settings import *
from src.utils import load_json_data, draw_text_with_outline, show_combo_effect
from src.food import spawn_food, load_images
from src.character import Character
from src.menu import main_menu
from src.popup import show_popup
from src.game_logic import handle_collisions, fade_in_out, next_round

# 초기 설정
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 배경 이미지 로드
background_imgs = [
    pygame.transform.scale(pygame.image.load(img_path), (WIDTH, HEIGHT)) for img_path in BACKGROUND_IMAGES
]

# JSON 데이터 로드
food_to_avoid = load_json_data("assets/data/foodToAvoid.json")
food_to_eat = load_json_data("assets/data/foodToEat.json")

images_foodToEat = load_images(food_to_eat, "assets/1Round/foodToEat")
images_foodToAvoid = load_images(food_to_avoid, "assets/1Round/foodToAvoid")

# 캐릭터 초기화
character = Character(375, 450)
good_face_duration = 300
good_face_timer = 0

# 메인 메뉴 실행
main_menu(screen, background_imgs[0], clock)

# 라운드 정보 초기화
rounds = [{"round": i, "required_food": food_to_eat, "avoid_food": food_to_avoid} for i in range(1, 4)]
current_round = 0
foods = []
game_data = {"eaten_food_count": 0, "eaten_foods": [], "score": 0, "lives": 3, "combo_count" : 0, "last_good_food_time" : 0}

# 라운드 루프
while current_round < len(rounds):
    # 배경 이미지 설정 (현재 라운드에 맞는 배경으로 설정)
    current_background = background_imgs[current_round + 1]  # +1을 추가하여 gym.png부터 시작

    # 라운드 시작 시 음식 생성 주기 조정
    if current_round > 0:  # 첫 번째 라운드는 기본 주기 사용
        SPAWN_INTERVAL = max(MIN_SPAWN_INTERVAL, SPAWN_INTERVAL - 50)

    # 라운드 시작 텍스트
    font = pygame.font.Font(FONT_PATH_SUBTITLE, FONT_SIZE_SUBTITLE)
    font2 = pygame.font.Font(FONT_PATH_TITLE, FONT_SIZE_TITLE)

    round_text = f"Round {current_round + 1}"
    screen.blit(current_background, (0, 0))
    draw_text_with_outline(screen, round_text, font, WHITE, BLACK,
                           WIDTH // 2 - font.size(round_text)[0] // 2,
                           HEIGHT // 2 - 50)
    pygame.display.flip()
    pygame.time.wait(3000)

    # 팝업 표시
    show_popup(screen, rounds[current_round], clock)

    # 게임 플레이 루프
    running = True
    combo_timer = 0     # 콤보 아직 시작 안함
    COMBO_TIMEOUT = 2000

    while running:
        current_time = pygame.time.get_ticks()
        screen.blit(current_background, (0, 0))

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # 키 입력 처리 및 캐릭터 이동
        keys = pygame.key.get_pressed()
        character.move(keys)

        # 음식 생성
        if current_time % SPAWN_INTERVAL == 0:
            foods.append(spawn_food(food_to_eat, food_to_avoid, images_foodToEat, images_foodToAvoid))

        # 캐릭터 및 음식 표시
        character.draw(screen)
        for food in foods[:]:
            food.update()
            food.draw(screen)
            if food.rect.top > HEIGHT:
                foods.remove(food)

        # 충돌 처리
        game_continues, good_food_eaten = handle_collisions(character, foods, game_data)
        if good_food_eaten:
            game_data["combo_count"] += 1
            character.set_image("assets/character/good_face.png")
            combo_timer = current_time
            good_face_timer = current_time

            if game_data["combo_count"] >= 2:
                show_combo_effect(screen, game_data["combo_count"], font2, clock, current_background)
        elif current_time - combo_timer > COMBO_TIMEOUT:
            game_data["combo_count"] = 0

            # good face 표시 시간 체크 및 기본 이미지로 복원
            if good_face_timer > 0 and current_time - good_face_timer >= good_face_duration:
                character.set_image("assets/character/base_face.png")  # 기본 이미지로 복원
                good_face_timer = 0  # 타이머 리셋

        if not game_continues:
            running = False
            # 게임 오버 처리
            game_over_text = "Game Over"
            draw_text_with_outline(screen, game_over_text, font, RED, BLACK,
                                   WIDTH // 2 - font.size(game_over_text)[0] // 2,
                                   HEIGHT // 2 - font.size(game_over_text)[1] // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        # 라운드 완료 조건 확인
        if game_data["eaten_food_count"] >= len(rounds[current_round]["required_food"]):
            current_round += 1
            if current_round >= len(rounds):
                game_clear_text = "Game Clear!"
                draw_text_with_outline(screen, game_clear_text, font, WHITE, BLACK,
                                       WIDTH // 2 - font.size(game_clear_text)[0] // 2,
                                       HEIGHT // 2 - font.size(game_clear_text)[1] // 2)
                pygame.display.flip()
                pygame.time.wait(3000)
            else:
                foods.clear()  # 다음 라운드를 위해 음식 초기화
                game_data["eaten_food_count"] = 0  # 다음 라운드를 위해 초기화
                game_data["eaten_foods"] = []  # 다음 라운드를 위해 초기화
            break

        # 점수 및 생명 표시 (테두리 추가)
        draw_text_with_outline(screen, f"Round {current_round + 1}", font, WHITE, BLACK, 10, 10)
        draw_text_with_outline(screen, f"Score: {game_data['score']}", font2, WHITE, BLACK, 10, 60)
        draw_text_with_outline(screen, f"Lives: {game_data['lives']}", font2, WHITE, BLACK,
                               WIDTH - font.size(f"Lives: {game_data['lives']}")[0] - 10, 10)
        draw_text_with_outline(screen, f"Combo: {game_data['combo_count']}", font2, WHITE, BLACK, 10, 110)
        pygame.display.flip()
        clock.tick(FPS)

    if not game_continues:
        break  # 게임 오버시 전체 게임 루프 종료

pygame.quit()