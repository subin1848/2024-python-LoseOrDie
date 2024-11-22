# 음식 생성 및 업데이트
import pygame, random, os
from .settings import WIDTH, HEIGHT

# 음식 객체 정의
class Food:
    def __init__(self, name, image, x, y, speed, is_good_food):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.is_good_food = is_good_food

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 음식 이미지 로딩 함수
def load_images(food_items, folder_path, size=(90, 90)):
    images = {}
    for food in food_items:
        food_image_path = os.path.join(folder_path, food["image"])
        image = pygame.image.load(food_image_path)
        image = pygame.transform.scale(image, size)
        images[food["name"]] = image
    return images

# 음식 생성 함수
def spawn_food(food_to_eat, food_to_avoid, images_foodToEat, images_foodToAvoid):
    is_good_food = random.choice([True, False])
    food_choice = random.choice(food_to_eat if is_good_food else food_to_avoid)
    image = images_foodToEat[food_choice["name"]] if is_good_food else images_foodToAvoid[food_choice["name"]]
    x = random.randint(0, WIDTH - image.get_width())
    y = -image.get_height()
    speed = random.randint(5, 10)
    return Food(food_choice["name"], image, x, y, speed, is_good_food)

# 랜덤 음식 3개 선택
# def select_random_foods(food_list, count=3):
#     return random.sample(food_list, count)

# 캐릭터와 음식의 충돌 여부
def handle_collisions(character, foods, game_data):
    for food in foods[:]:  # 리스트 복사본 순회
        if character.rect.colliderect(food.rect):  # 캐릭터와 음식 충돌 여부 확인
            if food.is_good_food:  # 여기에서 속성 이름 수정
                game_data["score"] += 1
            else:
                game_data["lives"] -= 1

            foods.remove(food)  # 충돌한 음식 제거

    return game_data["lives"] > 0
