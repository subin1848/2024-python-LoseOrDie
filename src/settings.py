# 게임 전역 설정
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
# 버튼
BUTTON_TEXT_COLOR = (255,255,255)
BUTTON_HOVER_COLOR = (255,0,0)

# 폰트 경로
FONT_PATH_TITLE = "assets/font/Dongle-Bold.ttf"
FONT_PATH_BODY = "assets/font/Dongle-Regular.ttf"
FONT_PATH_SUBTITLE = "assets/font/산돌광수.ttf"
FONT_SIZE_TITLE = 45
FONT_SIZE_BODY = 35
FONT_SIZE_SUBTITLE = 55
FONT_SMALL_SIZE_SUBTITLE = 35

# 타이머 설정
TIMER_LIMIT = 10
SPAWN_INTERVAL = 50    # 음식 생성 주기
MIN_SPAWN_INTERVAL = 20

BACKGROUND_IMAGES = [
    "assets/background/main.png",
    "assets/background/gym.png",
    "assets/background/myHome.png",
    "assets/background/date2_movie.png",
    "assets/background/date3_picnic.png"
]
