# 사용자 클래스 정의와 이동
import pygame
from .settings import WIDTH, HEIGHT

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/character/base_face.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # 캐릭터 이동 속도

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  # 왼쪽 방향키
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed  # 오른쪽 방향키

        # 화면 경계 내로 제한
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100,100))
# 캐릭터 초기화
character = Character(375, 450)

pygame.quit()