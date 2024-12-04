import pygame


class ImageButton:
    def __init__(self, image_path, x, y, scale=1.0, action=None):
        """
        Кнопка на основе изображения.
        :param image_path: Путь к файлу изображения кнопки.
        :param x: Координата X кнопки.
        :param y: Координата Y кнопки.
        :param scale: Масштаб кнопки (1.0 = оригинальный размер).
        :param action: Функция, которая выполняется при нажатии на кнопку.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (int(self.width * scale), int(self.height * scale))
        )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, screen):
        """
        Отрисовывает кнопку на экране.
        :param screen: Поверхность для рисования.
        """
        screen.blit(self.image, self.rect.topleft)

    def check_click(self, mouse_pos, mouse_click):
        """
        Проверяет, была ли нажата кнопка.
        :param mouse_pos: Позиция курсора мыши.
        :param mouse_click: Состояние кнопок мыши.
        """
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            if self.action:
                self.action()
