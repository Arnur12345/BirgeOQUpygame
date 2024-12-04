import pygame
import sys
from button import ImageButton  # Предполагается, что button.py уже существует с классом ImageButton
import time
import random
from poet_details import question_display_akhmet, question_display_ybyray,question_display_mirjakyp, question_display_mukhtar,question_display_tumanbay, question_display_zhansugirov, question_display_berdibek
from poet_details import question_display_batyrlar,question_display_ertegi,question_display_makal,question_display_sheshendik,question_display_zhanyltpash,question_display_zhumbak
from poet_details import question_display_abay, question_display_auezov,question_display_shakarim,question_display_nesipbek
from poet_details import question_display_akushtap, question_display_makhambet, question_display_qadyrmyrza

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIRGE OQU")

# Загрузка фоновой музыки
pygame.mixer.init()
try:
    pygame.mixer.music.load("arcade.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Воспроизведение музыки в бесконечном цикле
except pygame.error as e:
    print(f"Ошибка загрузки музыки: {e}")

# Загрузка изображений
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
gameplay_image = pygame.image.load("gameplay.jpg")  # Новый экран карты
gameplay_image = pygame.transform.scale(gameplay_image, (WIDTH, HEIGHT))

try:
    title_image = pygame.image.load("birgeoqu.png")
    button_image = pygame.image.load("button.png")
except FileNotFoundError:
    print("Файл с изображением не найден! Убедитесь, что birgeoqu.png, button.png и gameplay.jpg находятся в папке с кодом.")
    sys.exit()

# Масштабирование заголовка и кнопки
def scale_image(image, max_width, max_height):
    image_rect = image.get_rect()
    scale_ratio = min(max_width / image_rect.width, max_height / image_rect.height)
    new_width = int(image_rect.width * scale_ratio)
    new_height = int(image_rect.height * scale_ratio)
    return pygame.transform.scale(image, (new_width, new_height))

title_image = scale_image(title_image, WIDTH * 0.9, HEIGHT * 0.4)
button_image = scale_image(button_image, WIDTH * 0.4, HEIGHT * 0.1)  # Уменьшена кнопка

# Центрирование заголовка и кнопки
title_rect = title_image.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50))
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Регионы и поэты
regions_data = {
    "Батыс Қазақстан аймағы": {
        "background": "region_background/batysbg.jpg",
        "poets": ["Махамбет Өтемісұлы", "Қадыр Мырза Әлі", "Аққұштыа Бақтыгереева"]
    },
    "Онтүстік Қазақстан аймағы": {
        "background": "region_background/ontusticbg.jpg",
        "poets": ["Мұхтар Шаханов", "Бердібек Соқпақбаев", "Тұманбай Молдағалиев", "Ілияс Жансүгіров"]
    },
    "Орталық Қазақстан аймағы": {
        "background": "region_background/ortalyqbg.jpg",
        "poets": ["Ертегілер", "Жаңылтпаштар", "Батырлар жыры", "Шешендік сөздер", "Жұмбақтар", "Мақал-Мәтелдер"]
    },
    "Солтүстік Қазақстан аймағы": {
        "background": "region_background/soltusticbg.jpg",
        "poets": ["Ахмет Байтұрсынұлы","Ыбырай Алтынсарин", "Міржақып Дулатұлы"]
    },
    "Шығыс Қазақстан аймағы": {
        "background": "region_background/shygysbg.jpg",
        "poets": ["Абай Құнанбаев", "Шәкәрім Құдайбердіұлы", "Мұхтар Әуезов","Несіпбек  Айтұлы"]
    },
}

# Функции
def region_selected(region_name):
    global current_screen, selected_region
    selected_region = region_name
    current_screen = "region_info"



def display_poet_roulette(region_name):
    """
    Функция для отображения рулетки с поэтами.
    """
    screen.fill((0, 0, 0))
    region_data = regions_data[region_name]
    poets = region_data["poets"]
    background = pygame.image.load(region_data["background"])
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    start_time = time.time()
    selected_poet = None
    font = pygame.font.Font("pixel_font.ttf", 48)
    running = True

    while running:
        screen.blit(background, (0, 0))  # Отображаем фон
        elapsed_time = time.time() - start_time

        # Рулетка поэтов
        displayed_poet = random.choice(poets)
        poet_surface = font.render(displayed_poet, True, (255, 255, 255))
        poet_x = WIDTH // 2 - poet_surface.get_width() // 2
        poet_y = HEIGHT // 2 - poet_surface.get_height() // 2

        # Отображение текущего поэта
        screen.blit(poet_surface, (poet_x, poet_y))
        pygame.display.flip()
        time.sleep(0.1)  # Скорость прокрутки

        if elapsed_time > 5:  # Остановка рулетки через 5 секунд
            selected_poet = displayed_poet
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Проверяем выпавшего поэта
    if selected_poet == "Ахмет Байтұрсынұлы":
        question_display_akhmet.display()
    elif selected_poet == "Ыбырай Алтынсарин":
        question_display_ybyray.display()
    elif selected_poet == "Міржақып Дулатұлы":
        question_display_mirjakyp.display()
    elif selected_poet == "Мұхтар Шаханов":
        question_display_mukhtar.display()
    elif selected_poet == "Ілияс Жансүгіров":
        question_display_zhansugirov.display()
    elif selected_poet == "Бердібек Соқпақбаев":
        question_display_berdibek.display()
    elif selected_poet == "Тұманбай Молдағалиев":
        question_display_tumanbay.display()

    #central

    elif selected_poet == "Ертегілер":
        question_display_ertegi.display()
    elif selected_poet == "Жаңылтпаштар":
        question_display_zhanyltpash.display()
    elif selected_poet == "Батырлар жыры":
        question_display_batyrlar.display()
    elif selected_poet == "Шешендік сөздер":
        question_display_sheshendik.display()
    elif selected_poet == "Жұмбақтар":
        question_display_zhumbak.display()
    elif selected_poet == "Мақал-Мәтелдер":
        question_display_makal.display()
        
    #west
    elif selected_poet == "Абай Құнанбаев":
        question_display_abay.display()
    elif selected_poet == "Шәкәрім Құдайбердіұлы":
        question_display_shakarim.display()
    elif selected_poet == "Мұхтар Әуезов":
        question_display_auezov.display()
    elif selected_poet == "Несіпбек  Айтұлы":
        question_display_nesipbek.display()

    #east
    elif selected_poet == "Махамбет Өтемісұлы":
        question_display_nesipbek.display()
    elif selected_poet == "Қадыр Мырза Әлі":
        question_display_nesipbek.display()
    elif selected_poet == "Аққұштыа Бақтыгереева":
        question_display_nesipbek.display()

    return selected_poet

# Кнопки для регионов с изображениями
buttons = [
    ImageButton("aimaq/batys.png", 200, 300, 0.3, lambda: region_selected("Батыс Қазақстан аймағы")),
    ImageButton("aimaq/ontustic.png", 700, 550, 0.3, lambda: region_selected("Онтүстік Қазақстан аймағы")),
    ImageButton("aimaq/ortalyq.png", 650, 350, 0.3, lambda: region_selected("Орталық Қазақстан аймағы")),
    ImageButton("aimaq/soltustic.png", 680, 150, 0.3, lambda: region_selected("Солтүстік Қазақстан аймағы")),
    ImageButton("aimaq/shygys.png", 950, 300, 0.3, lambda: region_selected("Шығыс Қазақстан аймағы")),
]

# Игровые состояния
current_screen = "menu"  # Стартовый экран
selected_region = None  # Выбранный регион

# Шрифт
font = pygame.font.SysFont("pixel_font.ttf", 36)

# Основной цикл
running = True
while running:
    screen.fill((0, 0, 0))  # Чёрный фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu" and button_rect.collidepoint(event.pos):  # Переход к карте
                current_screen = "map"
            elif current_screen == "map":
                for button in buttons:
                    button.check_click(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and current_screen == "region_info":  # Вернуться на карту
                current_screen = "map"

    if current_screen == "menu":
        # Отображение стартового экрана
        screen.blit(background, (0, 0))
        screen.blit(title_image, title_rect)
        screen.blit(button_image, button_rect)

    elif current_screen == "map":
        # Отображение карты
        screen.blit(gameplay_image, (0, 0))
        for button in buttons:
            button.draw(screen)

    elif current_screen == "region_info":
        # Рулетка поэтов
        selected_poet = display_poet_roulette(selected_region)
        print(f"Выбранный поэт: {selected_poet}")
        current_screen = "map"

    pygame.display.flip()

pygame.quit()
sys.exit()
