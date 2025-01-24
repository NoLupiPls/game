import pygame


class Menu:
    def __init__(self, screen, start_game_callback):
        """
        Инициализация меню.
        :param screen: Экран для отрисовки меню.
        """
        self.screen = screen
        self.options = [
            {"label": "Продолжить", "action": self.resume_game, "enabled": False},
            {"label": "Новая игра", "action": self.new_game, "enabled": True},
            {"label": "Уровни", "action": self.show_levels, "enabled": True},
            {"label": "Настройки", "action": self.show_settings, "enabled": True},
            {"label": "Выход", "action": self.quit_game, "enabled": True},
        ]
        self.selected_index = 1  # Выбор по умолчанию
        self.font = pygame.font.Font("assets/fonts/comic_sans_pixel.ttf", 24)  # Шрифт
        self.base_color = (255, 255, 255)
        self.hover_color = (200, 200, 255)
        self.disabled_color = (100, 100, 100)
        self.spacing = 50  # Расстояние между кнопками
        self.start_x = 30  # Отступ слева
        self.start_y = 100  # Начальная позиция кнопок
        self.running = True  # Состояние работы меню
        self.settings = None
        self.start_game_callback = start_game_callback

    def render_text(self, text, color):
        """Создаёт текстовую поверхность."""
        return self.font.render(text, True, color)

    def handle_input(self, events):
        """Обрабатывает ввод с мыши и клавиатуры."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Стрелка вверх
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:  # Стрелка вниз
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:  # Enter
                    if self.options[self.selected_index]["enabled"]:
                        self.options[self.selected_index]["action"]()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    mouse_pos = pygame.mouse.get_pos()
                    for index, option in enumerate(self.options):
                        label_surface = self.render_text(option["label"], self.base_color)
                        label_rect = label_surface.get_rect(topleft=(self.start_x, self.start_y + index * self.spacing))
                        if label_rect.collidepoint(mouse_pos) and option["enabled"]:
                            option["action"]()
            elif event.type == pygame.MOUSEWHEEL:  # Прокрутка колесика мыши
                if event.y > 0:  # Прокрутка вверх
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.y < 0:  # Прокрутка вниз
                    self.selected_index = (self.selected_index + 1) % len(self.options)

        # Обработка движения мыши
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            label_surface = self.render_text(option["label"], self.base_color)
            label_rect = label_surface.get_rect(topleft=(self.start_x, self.start_y + index * self.spacing))
            if label_rect.collidepoint(mouse_pos):
                self.selected_index = index

    def draw(self):
        """Отрисовывает меню."""
        self.screen.fill((0, 0, 0))  # Фон
        for index, option in enumerate(self.options):
            # Цвет текста
            if not option["enabled"]:
                color = self.disabled_color
            elif index == self.selected_index:
                color = self.hover_color
            else:
                color = self.base_color

            # Анимация текста (смещение при наведении)
            x_offset = 10 if index == self.selected_index else 0
            label_surface = self.render_text(option["label"], color)
            self.screen.blit(label_surface, (self.start_x + x_offset, self.start_y + index * self.spacing))
        pygame.display.flip()

    def run(self):
        """Запуск меню."""
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()

            # Обработка ввода
            self.handle_input(events)

            # Рисуем меню
            self.draw()
            clock.tick(60)

    # Методы действий меню
    def resume_game(self):
        print("Игра продолжается!")
        # Добавьте здесь логику для продолжения игры
        self.running = False

    def new_game(self):
        print("Начинается новая игра!")
        # Добавьте здесь логику для запуска новой игры
        self.start_game_callback()

    def show_levels(self):
        print("Меню уровней!")
        # Добавьте здесь логику для отображения уровней
        self.running = False

    def show_settings(self):
        print("Меню настроек!")
        # Добавьте здесь логику для отображения настроек
        self.open_settings()

    def quit_game(self):
        print("Выход из игры!")
        self.running = False
        pygame.quit()
        exit()

    def open_settings(self):
        """Открывает экран настроек."""
        if not self.settings:  # Если настройки еще не созданы
            from ui.settings import Settings  # Импортируем класс Settings
            self.settings = Settings(self.screen)  # Создаем объект настроек
        self.settings.run()
