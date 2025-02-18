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
        """
        self.screen = screen
        self.questions = questions_data
        self.background_path = background_path
        self.poet_path = poet_path
        self.font = pygame.font.Font("intro.ttf", 36)  # Уменьшен размер шрифта
        self.timer_font = pygame.font.Font("intro.ttf", 24)  # Меньший шрифт для таймера
        self.button_font = pygame.font.Font("intro.ttf", 28)  # Уменьшен размер шрифта кнопок
        self.button_width = 400  # Уменьшена ширина кнопок
        self.button_height = 60  # Уменьшена высота кнопок
        self.button_margin = 20  # Уменьшен отступ между кнопками
        self.completed_degrees = set()
        self.text_input_width = 600  # Увеличена ширина поля ввода
        self.text_input_height = 100  # Увеличена высота поля ввода
        self.max_chars_per_line = 70  # Максимальное количество символов в строке

    def display(self):
        """
        Запускает процесс отображения уровней и вопросов.
        """
        self.display_poet_image()
        while len(self.completed_degrees) < 5:
            selected_degree = self.display_degree_selection()
            self.display_questions_by_degree(selected_degree)
        self.display_completion_message()

    def display_degree_selection(self):
        """
        Отображает кнопки для выбора уровня вопросов на фоне.
        """
        degrees = ["Білемін", "Түсінемін", "Қолданамын", "Талдаймын", "Жинақтаймын"]
        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        buttons = []

        start_y = HEIGHT // 4 + 50  

        for i, degree in enumerate(degrees):
            button_rect = pygame.Rect(
                WIDTH // 2 - self.button_width // 2,
                start_y + i * (self.button_height + self.button_margin),
                self.button_width,
                self.button_height
            )
            buttons.append((button_rect, degree))

        selected_degree = None
        while not selected_degree:
            self.screen.blit(background, (0, 0))
            for button_rect, degree in buttons:
                color = (0, 255, 0) if degree in self.completed_degrees else (50, 50, 50)
                pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
                pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3, border_radius=15)
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
                        if button_rect.collidepoint(event.pos) and degree not in self.completed_degrees:
                            selected_degree = degree

        return selected_degree

    def display_questions_by_degree(self, degree):
        """
        Отображает вопросы, относящиеся к выбранному уровню.
        """
        filtered_questions = [q for q in self.questions if q.get("degree") == degree]
        for question_data in filtered_questions:
            self.display_question(question_data)
        self.completed_degrees.add(degree)

    def display_poet_image(self):
        """
        Отображает изображение поэта на экране с обратным отсчетом в течение 10 секунд.
        """
        poet_image = pygame.image.load(self.poet_path)
        poet_image = pygame.transform.scale(poet_image, (WIDTH, HEIGHT))
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(0, 10 - elapsed_time)

            if remaining_time == 0:
                running = False

            self.screen.blit(poet_image, (0, 0))
            timer_text = f"Уақыты: {remaining_time} с"
            timer_surface = self.timer_font.render(timer_text, True, (255, 255, 255))

            timer_x = 20
            timer_y = 20
            self.screen.blit(timer_surface, (timer_x, timer_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.delay(100)

    def draw_multiline_text(self, surface, text, x, y, font, color, max_chars_per_line=70, line_spacing=10):
        """
        Рисует текст с переносом по количеству символов.
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)
            if current_length + word_length + len(current_line) <= max_chars_per_line:
                current_line.append(word)
                current_length += word_length
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length

        if current_line:
            lines.append(" ".join(current_line))

        total_height = len(lines) * (font.get_height() + line_spacing)
        start_y = y - (total_height // 2)

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            line_width = line_surface.get_width()
            line_x = x - (line_width // 2)
            surface.blit(line_surface, (line_x, start_y + i * (font.get_height() + line_spacing)))

    def display_question(self, question_data):
        """
        Отображает один вопрос с переносом текста и таймером.
        """
        question_text = question_data.get("question", "Вопрос отсутствует")
        options = question_data.get("options", [])
        correct_answer = question_data.get("correct", None)
        degree = question_data.get("degree", "")
        is_text_question = not options and degree != "Жұмбақтар"

        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        running = True
        user_text = ""
        input_box = pygame.Rect(
            WIDTH // 2 - self.text_input_width // 2,
            HEIGHT // 2,
            self.text_input_width,
            self.text_input_height
        )

        timer_seconds = 10 if degree == "Жұмбақтар" else 15
        start_time = pygame.time.get_ticks()

        buttons = []
        if not is_text_question and degree != "Жұмбақтар":
            start_y = HEIGHT // 2 + 30  # Сдвигаем кнопки ниже
            for i, option in enumerate(options):
                button_rect = pygame.Rect(
                    WIDTH // 2 - self.button_width // 2,
                    start_y + i * (self.button_height + self.button_margin),
                    self.button_width,
                    self.button_height
                )
                buttons.append((button_rect, option))

        selected_answer = None

        while running:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(0, timer_seconds - elapsed_time)

            self.screen.blit(background, (0, 0))

            timer_surface = self.timer_font.render(f"Уақыты: {remaining_time} с", True, (255, 0, 0))
            timer_x = 20
            timer_y = 20
            self.screen.blit(timer_surface, (timer_x, timer_y))

            self.draw_multiline_text(
                self.screen,
                question_text,
                x=WIDTH // 2,
                y=HEIGHT // 4,  # Выводим вопрос выше
                font=self.font,
                color=(255, 255, 255),
                max_chars_per_line=self.max_chars_per_line
            )

            if remaining_time == 0:
                running = False
                if degree == "Жұмбақтар":
                    self.display_result_text_question("Уақыт аяқталды!")
                elif is_text_question:
                    self.display_result_text_question(user_text)
                else:
                    self.display_result(None, correct_answer)

            if is_text_question:
                pygame.draw.rect(self.screen, (255, 255, 255), input_box, border_radius=10)
                text_surface = self.font.render(user_text, True, (0, 0, 0))
                self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            elif degree != "Жұмбақтар":
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

    def display_completion_message(self):
        """
        Отображает сообщение, когда все уровни завершены.
        """
        background = pygame.image.load(self.background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        message_surface = self.font.render("Барлық деңгейлер аяқталды!", True, (0, 255, 0))
        message_x = WIDTH // 2 - message_surface.get_width() // 2
        message_y = HEIGHT // 2 - message_surface.get_height() // 2
        self.screen.blit(message_surface, (message_x, message_y))
        pygame.display.flip()
        time.sleep(5)

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