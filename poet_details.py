import pygame
import sys
import time
from questions import akhmet_questions, ybyray_questions, mirjakyp_questions, mukhtar_questions,zhansugirov_questions, tumanbay_questions, berdibek_questions
from questions import ertegi_questions, zhanyltpash_questions, batyrlar_zhyry_questions,  zhumbak_questions, sheshendik_soz_questions,makal_questions
from questions import abay_questions, shakarim_questions, auezov_questions, nesipbek_questions
from questions import makhambet_questions, akushtap_questions, qadyrmyrza_questions

WIDTH, HEIGHT = 1280, 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIRGE OQU")

class QuestionDisplay:
    def __init__(self, screen, questions_data, background_path, poet_path):
        """
        Класс для отображения вопросов и вариантов ответов.

        :param screen: Экран Pygame.
        :param questions_data: Список словарей с вопросами, вариантами и правильными ответами.
        :param background_path: Путь к изображению фона для вопросов.
        :param poet_path: Путь к изображению поэта.
        """
        self.screen = screen
        self.questions = questions_data
        self.background_path = background_path
        self.poet_path = poet_path
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        self.button_width = 400
        self.button_height = 60
        self.button_margin = 20

    def display(self):
        """
        Отображает картину поэта на 10 секунд, затем предлагает выбрать уровень вопроса.
        """
        self.display_poet_image()
        selected_degree = self.display_degree_selection()
        self.display_questions_by_degree(selected_degree)

    def display_poet_image(self):
        """
        Отображает картину поэта на 10 секунд.
        """
        poet_image = pygame.image.load(self.poet_path)
        poet_image = pygame.transform.scale(poet_image, (WIDTH, HEIGHT))
        end_time = time.time() + 10  # 10 секунд для отображения
        font = pygame.font.Font(None, 48)

        while time.time() < end_time:
            self.screen.fill((0, 0, 0))
            self.screen.blit(poet_image, (0, 0))

            # Отображение таймера
            remaining_time = int(end_time - time.time())
            timer_text = f"{remaining_time} секунд"
            timer_surface = font.render(timer_text, True, (255, 255, 255))
            self.screen.blit(timer_surface, (20, 20))

            pygame.display.flip()
            time.sleep(1)

    def display_degree_selection(self):
        """
        Отображает кнопки для выбора уровня вопросов на фоне.
        """
        degrees = ["Білемін", "Түсінемін", "Қолданамын", "Талдаймын", "Жинақтаймын"]
        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        buttons = []

        for i, degree in enumerate(degrees):
            button_rect = pygame.Rect(WIDTH // 2 - self.button_width // 2,
                                       200 + i * (self.button_height + self.button_margin),
                                       self.button_width,
                                       self.button_height)
            buttons.append((button_rect, degree))

        selected_degree = None
        while not selected_degree:
            self.screen.blit(background, (0, 0))
            for button_rect, degree in buttons:
                pygame.draw.rect(self.screen, (50, 50, 50), button_rect, border_radius=10)
                pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2, border_radius=10)
                text_surface = self.button_font.render(degree, True, (255, 255, 255))
                text_x = button_rect.centerx - text_surface.get_width() // 2
                text_y = button_rect.centery - text_surface.get_height() // 2
                self.screen.blit(text_surface, (text_x, text_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, degree in buttons:
                        if button_rect.collidepoint(event.pos):
                            selected_degree = degree

        return selected_degree

    def display_questions_by_degree(self, degree):
        """
        Отображает вопросы, относящиеся к выбранному уровню.
        """
        filtered_questions = [q for q in self.questions if q.get("degree") == degree]
        for question_data in filtered_questions:
            self.display_question(question_data)

    def display_question(self, question_data):
        """
        Отображает один вопрос на фоне `questions.jpg` с таймером на 15 секунд.
        Для категории "Жұмбақтар" текстового поля нет, только 10-секундный таймер.
        """
        question_text = question_data.get("question", "Вопрос отсутствует")
        options = question_data.get("options", [])
        correct_answer = question_data.get("correct", None)
        degree = question_data.get("degree", "")
        is_text_question = not options and degree != "Жұмбақтар"  # Для "Жұмбақтар" всегда отключаем текстовое поле

        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        running = True
        user_text = ""  # Для текстового ответа
        input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 50)

        # Таймер
        timer_seconds = 10 if degree == "Жұмбақтар" else 15
        start_time = pygame.time.get_ticks()

        # Расчёт позиций кнопок (если это не текстовый вопрос)
        buttons = []
        if not is_text_question and degree != "Жұмбақтар":
            start_y = HEIGHT // 2 - (len(options) * (self.button_height + self.button_margin)) // 2
            for i, option in enumerate(options):
                button_rect = pygame.Rect(
                    WIDTH // 2 - self.button_width // 2,
                    start_y + i * (self.button_height + self.button_margin),
                    self.button_width,
                    self.button_height
                )
                buttons.append((button_rect, option))

        selected_answer = None  # Для фиксации выбора пользователя

        while running:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(0, timer_seconds - elapsed_time)

            self.screen.blit(background, (0, 0))

            # Отображение таймера
            timer_surface = self.font.render(f"Уақыты: {remaining_time} секунд", True, (255, 0, 0))
            timer_x = WIDTH // 2 - timer_surface.get_width() // 2
            timer_y = HEIGHT // 5
            self.screen.blit(timer_surface, (timer_x, timer_y))

            # Отображение вопроса
            question_surface = self.font.render(question_text, True, (255, 255, 255))
            question_x = WIDTH // 2 - question_surface.get_width() // 2
            question_y = HEIGHT // 3 - question_surface.get_height() // 2-35
            self.screen.blit(question_surface, (question_x, question_y))

            if remaining_time == 0:  # Если время вышло
                running = False
                if degree == "Жұмбақтар":
                    self.display_result_text_question("Уақыт аяқталды!")
                elif is_text_question:
                    self.display_result_text_question(user_text)
                else:
                    self.display_result(None, correct_answer)

            if is_text_question:
                # Текстовый ввод
                pygame.draw.rect(self.screen, (255, 255, 255), input_box, border_radius=10)
                text_surface = self.font.render(user_text, True, (0, 0, 0))
                self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            elif degree != "Жұмбақтар":
                # Кнопки ответов
                for button_rect, option in buttons:
                    pygame.draw.rect(self.screen, (50, 50, 50), button_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2, border_radius=10)
                    option_surface = self.button_font.render(option, True, (255, 255, 255))
                    option_x = button_rect.centerx - option_surface.get_width() // 2
                    option_y = button_rect.centery - option_surface.get_height() // 2
                    self.screen.blit(option_surface, (option_x, option_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if is_text_question and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                elif not is_text_question and degree != "Жұмбақтар" and event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, option in buttons:
                        if button_rect.collidepoint(event.pos):
                            selected_answer = option
                            running = False

        if not is_text_question and degree != "Жұмбақтар":
            self.display_result(selected_answer, correct_answer)


    def display_result(self, selected_answer, correct_answer):
        """
        Отображает результат ответа (правильный или неправильный).
        """
        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        result_text = "Дұрыс!" if selected_answer == correct_answer else f"Қате! Дұрыс жауап: {correct_answer}"
        result_surface = self.font.render(result_text, True, (0, 255, 0) if selected_answer == correct_answer else (255, 0, 0))
        result_x = WIDTH // 2 - result_surface.get_width() // 2
        result_y = HEIGHT // 2 - result_surface.get_height() // 2
        self.screen.blit(result_surface, (result_x, result_y))
        pygame.display.flip()
        time.sleep(3)

    def display_result_text_question(self, user_text):
        """
        Показывает сообщение после текстового ответа.
        """
        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        result_text = f"Сіздің жауабыныз: {user_text}"
        result_surface = self.font.render(result_text, True, (255, 255, 255))
        result_x = WIDTH // 2 - result_surface.get_width() // 2
        result_y = HEIGHT // 2 - result_surface.get_height() // 2
        self.screen.blit(result_surface, (result_x, result_y))
        pygame.display.flip()
        time.sleep(3)

#north
question_display_akhmet = QuestionDisplay(
    screen=screen,
    questions_data=akhmet_questions,
    background_path="poembg/north/akhmet/questions.jpg",
    poet_path="poembg/north/akhmet/akhmetbay.jpg"
)
question_display_ybyray = QuestionDisplay(
    screen=screen,
    questions_data=ybyray_questions,
    background_path="poembg/north/ybyray/questions.jpg",
    poet_path="poembg/north/ybyray/ybyray.jpg"
)

question_display_mirjakyp = QuestionDisplay(
    screen=screen,
    questions_data=mirjakyp_questions,
    background_path="poembg/north/mirjakyp/questions.jpg",
    poet_path="poembg/north/mirjakyp/mirjakyp.jpg"
)

#south
question_display_mukhtar = QuestionDisplay(
    screen=screen, 
    questions_data=mukhtar_questions,
    background_path="poembg/south/mukhtar/questions.jpg",
    poet_path="poembg/south/mukhtar/mukhtar.jpg"
)


question_display_zhansugirov = QuestionDisplay(
    screen=screen, 
    questions_data=zhansugirov_questions,
    background_path="poembg/south/zhansugirov/questions.jpg",
    poet_path="poembg/south/zhansugirov/zhansugirov.jpg"
)
question_display_tumanbay = QuestionDisplay(
    screen=screen, 
    questions_data=tumanbay_questions,
    background_path="poembg/south/tumanbay/questions.jpg",
    poet_path="poembg/south/tumanbay/tumanbay.jpg"
)

question_display_berdibek = QuestionDisplay(
    screen=screen, 
    questions_data=berdibek_questions,
    background_path="poembg/south/berdibek/questions.jpg",
    poet_path="poembg/south/berdibek/berdibek.jpg"
)

#central
question_display_batyrlar = QuestionDisplay(
    screen=screen, 
    questions_data=batyrlar_zhyry_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/batyrlar.jpg"
)
question_display_ertegi = QuestionDisplay(
    screen=screen, 
    questions_data=ertegi_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/ertegi.jpg"
)

question_display_sheshendik = QuestionDisplay(
    screen=screen, 
    questions_data=sheshendik_soz_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/sheshendik.jpg"
)

question_display_zhanyltpash = QuestionDisplay(
    screen=screen, 
    questions_data=zhanyltpash_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/zhanyltpash.jpg"
)

question_display_zhumbak = QuestionDisplay(
    screen=screen, 
    questions_data=zhumbak_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/zhumbak.jpg"
)
question_display_makal = QuestionDisplay(
    screen=screen, 
    questions_data=makal_questions,
    background_path="poembg/central/questions.jpg",
    poet_path="poembg/central/makal.jpg"
)

#west

question_display_abay = QuestionDisplay(
    screen=screen, 
    questions_data=abay_questions,
    background_path="poembg/west/questions.jpg",
    poet_path="poembg/west/abay.jpg"
)
question_display_shakarim = QuestionDisplay(
    screen=screen, 
    questions_data=shakarim_questions,
    background_path="poembg/west/questions.jpg",
    poet_path="poembg/west/shakarim.jpg"
)
question_display_auezov = QuestionDisplay(
    screen=screen, 
    questions_data=auezov_questions,
    background_path="poembg/west/questions.jpg",    
    poet_path="poembg/west/auezov.jpg"
)
question_display_nesipbek = QuestionDisplay(
    screen=screen, 
    questions_data=nesipbek_questions,
    background_path="poembg/west/questions.jpg",
    poet_path="poembg/west/nesipbek.jpg"
)
#east
question_display_akushtap = QuestionDisplay(
    screen=screen, 
    questions_data=akushtap_questions,
    background_path="poembg/east/questions.jpg",
    poet_path="poembg/east/akushtap.jpg"
)
question_display_makhambet = QuestionDisplay(
    screen=screen, 
    questions_data=makhambet_questions,
    background_path="poembg/east/questions.jpg",
    poet_path="poembg/east/makhambet.jpg"
)
question_display_qadyrmyrza = QuestionDisplay(
    screen=screen, 
    questions_data=qadyrmyrza_questions,
    background_path="poembg/east/questions.jpg",
    poet_path="poembg/east/qadyrmyrza.jpg"
)