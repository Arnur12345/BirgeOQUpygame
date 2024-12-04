import pygame
import time
import random
import sys

def region_screen(screen, background_image, region_name, poets):
    """
    Функция отображения экрана региона с рулеткой поэтов.
    :param screen: Экран Pygame
    :param background_image: Фон региона
    :param region_name: Название региона
    :param poets: Список поэтов
    """
    running = True
    selected_poet = None
    scroll_speed = 0.2
    start_time = time.time()

    # Загрузка кастомного шрифта pixel_font.ttf
    try:
        font = pygame.font.Font("pixel_font.ttf", 36)
    except FileNotFoundError:
        print("Файл pixel_font.ttf не найден! Убедитесь, что он находится в папке проекта.")
        sys.exit()

    # Загрузка фона региона
    bg_image = pygame.image.load(background_image)
    bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))

    while running:
        screen.blit(bg_image, (0, 0))  # Рисуем фон
        current_time = time.time()

        # Прокрутка поэтов
        random.shuffle(poets)
        displayed_poet = poets[0]

        # Текст региона
        title_surface = font.render(f"Регион: {region_name}", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        # Текст поэта
        poet_surface = font.render(displayed_poet, True, (255, 255, 255))
        screen.blit(poet_surface, (screen.get_width() // 2 - poet_surface.get_width() // 2, screen.get_height() // 2))

        pygame.display.flip()
        time.sleep(scroll_speed)

        # Увеличиваем задержку перед остановкой
        if current_time - start_time > 4:
            scroll_speed += 0.05
            if scroll_speed >= 1.0:
                running = False
                selected_poet = displayed_poet

        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    return selected_poet
