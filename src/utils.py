# 유틸리티 함수 (이미지 로드, json 저장)
import json
import pygame

# json 데이터 저장
def save_to_json(data, filepath="game_data.json"):
    with open(filepath, "w") as f:
        json.dump(data, f)

# json 파일 로드
def load_json_data(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

# 이미지 로드
def load_images(food_items, folder_path, size=(90, 90)):
    images = {}
    for food in food_items:
        image_path = f"{folder_path}/{food['image']}"
        image = pygame.image.load(image_path)
        images[food["name"]] = pygame.transform.scale(image, size)
    return images

# 텍스트 border
def draw_text_with_outline(surface, text, font, text_color, outline_color, x, y):
    outline_surfaces = []
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        s = font.render(text, True, outline_color)
        outline_surfaces.append((s, (x + dx, y + dy)))

    text_surface = font.render(text, True, text_color)

    for s, pos in outline_surfaces:
        surface.blit(s, pos)

    surface.blit(text_surface, (x, y))

# 콤보 효과
def show_combo_effect(surface, combo_count, font, clock, current_background):
    if combo_count >= 2:
        combo_text = f"{combo_count} COMBO!"
        text_color = (255, 255, 0)  # 노란색
        outline_color = (255, 0, 0)  # 빨간색

        base_font_size = font.get_height()

        # 콤보 효과
        for scale in [2.0, 1.8, 1.6, 1.4, 1.2, 1.0]:
            scaled_size = int(base_font_size * scale)
            scaled_font = pygame.font.Font(None, scaled_size)
            text_width, text_height = scaled_font.size(combo_text)
            x = (surface.get_width() - text_width) // 2
            y = (surface.get_height() - text_height) // 2

            surface.blit(current_background, (0, 0))  # 현재 배경을 다시 그림

            # 콤보 텍스트 그리기
            draw_text_with_outline(surface, combo_text, scaled_font, text_color, outline_color, x, y)
            pygame.display.flip()
            pygame.time.wait(50)  # 각 프레임 사이에 짧은 대기 시간 추가

        pygame.time.wait(300)  # 콤보 텍스트를 잠시 표시

        # 페이드 아웃 효과
        fade_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        for alpha in range(0, 255, 15):
            fade_surface.fill((0, 0, 0, alpha))
            surface.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(20)