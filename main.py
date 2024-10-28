import random
import pygame

from src import WIDTH, HEIGHT, FPS, BACKGROUND_IMAGES

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("빼지 못하면 죽음 뿐")
clock = pygame.time.Clock()

# 폰트 초기화
font = pygame.font.SysFont('Noto Sans', 24)

#TODO: 이 함수 찾아보기
def scale_background_image(image, width, height):
    img_width, img_height = image.get_size()
    aspect_ratio = img_width / img_height

    if width / height > aspect_ratio:
        new_width = height * aspect_ratio
        new_height = height
    else:
        new_width = width
        new_height = width / aspect_ratio

    return pygame.transform.scale(image, (int(new_width), int(new_height)))
#TODO: 이 함수 찾아보기
def draw_rounded_rect(surface, color, rect, radius):
    x, y, width, height = rect

    # 사각형 그리기
    pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))

    # 둥근 모서리 그리기
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)

# 초기 라운드 설정
current_round = 1
background_image = scale_background_image(pygame.image.load(BACKGROUND_IMAGES[current_round]), WIDTH, HEIGHT)

# 1라운드(헬스장) 먹어야될 음식, 먹으면 안될 음식
food_to_eat = ["닭가슴살", "고구마", "단백질 쉐이크", "삶은 계란", "아몬드", "단백질 바"]
food_to_avoid = "탄산음료"

# 음식 배열
eaten_food = []

# 먹은 음식 수
eaten_food_count = 0

# 랜덤 음식 3개
must_eat_food = random.sample(food_to_eat, 3)

# 라운드 시간 설정
timer_limit = 40
start_time = pygame.time.get_ticks()

# 게임루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = (pygame.time.get_ticks() - start_time) / 1000

    # 게임 로직 업데이트
    if current_time < timer_limit:
        # TODO: 사용자가 음식을 먹을 때 호출되는 로직 추가
        keys = pygame.key.get_pressed()
        # 사용자가 음식을 먹음
        if keys[pygame.K_UP]:
            food = random.choice(food_to_eat + [food_to_avoid])
            eaten_food.append(food)
            # 먹어야 할 음식, 먹으면 안되는 음식 카운트 증가
            if food == food_to_eat:
                eaten_food_count += 1
            if food == food_to_avoid:
                running = False

    else:
        # 제한 시간이 끝났을 때 라운드 증가
        if eaten_food_count >= 3:
            current_round += 1
            # 다음 라운드의 인덱스를 계산
            next_round_index = (current_round % len(BACKGROUND_IMAGES))
            background_image = pygame.image.load(BACKGROUND_IMAGES[next_round_index], WIDTH, HEIGHT)
            eaten_food_count = 0
            eaten_food.clear()
            start_time = pygame.time.get_ticks()
        else:
            running = False

    screen.fill((0, 0, 0))  # 화면을 검은색으로 초기화
    screen.blit(background_image, (0, 0))  # 배경 이미지 그리기

    # 랜덤 음식 보여주는 박스 그리기
    box_width = 680
    box_height = 360
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    box_radius = 20

    draw_rounded_rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), box_radius)

    # 먹어야 할 음식 텍스트
    must_eat_food_text = "먹어야 할 음식: " + ", " .join(must_eat_food);
    avoid_food_text = "먹으면 안되는 음식: " + food_to_avoid

    # 텍스트 렌더링
    must_eat_surface = font.render(must_eat_food_text, True, (0,0,0))
    avoid_food_surface = font.render(avoid_food_text, True, (255,0,0))
    # 텍스트 위치 설정
    screen.blit(must_eat_surface, (box_x + 10, box_y + 10))
    screen.blit(avoid_food_surface, (box_x + 10, box_y + 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()