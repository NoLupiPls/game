import pygame
import sys

from core.settings import WIDTH, HEIGHT


class SettingsPage:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/comic_sans_pixel.ttf", 28)
        self.tabs = ["Звук и музыка", "Графика", "Управление", "Назад"]
        self.current_tab = 0
        self.left_block_selected = True  # Выбор в левой панели
        self.right_block_selected = False  # Выбор в правой панели
        self.current_parameter = 0  # Индекс активного параметра в правом блоке
        self.menu = None

        # Параметры вкладок
        self.sound_settings = {
            "Громкость музыки": 50,
            "Громкость звуков": 50
        }
        self.graphics_settings = {
            "Режим экрана": ["Оконный", "Полноэкранный"],
            "Разрешение": ["1920x1080", "1280x720", "800x600"],
            "Кол-во кадров": ["30", "60", "120"]
        }
        self.current_graphics_values = {
            "Режим экрана": "Оконный",
            "Разрешение": "1920x1080",
            "Кол-во кадров": "60"
        }

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """Отображение текста на экране."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_tabs(self):
        """Отображение вкладок (включая кнопку Назад)."""
        for i, tab in enumerate(self.tabs):
            color = (200, 200, 255) if i == self.current_tab else (255, 255, 255)
            self.draw_text(tab, 30, 100 + i * 50, color)

    def draw_sound_tab(self):
        """Отображение настроек звука."""
        y_offset = 100
        for i, (setting, value) in enumerate(self.sound_settings.items()):
            color = (200, 200, 255) if self.right_block_selected and self.current_parameter == i else (255, 255, 255)
            self.draw_text(f"{setting}: {value}%", 300, y_offset, color)

            # Отображение полосы громкости
            pygame.draw.rect(self.screen, (40, 40, 40), (300, y_offset + 30, 200, 10))
            pygame.draw.rect(self.screen, (255, 255, 255), (300, y_offset + 30, value * 2, 10))
            y_offset += 80

    def draw_graphics_tab(self):
        """Отображение настроек графики."""
        y_offset = 100
        for i, (setting, options) in enumerate(self.graphics_settings.items()):
            current_value = self.current_graphics_values[setting]
            color = (200, 200, 255) if self.right_block_selected and self.current_parameter == i else (255, 255, 255)
            self.draw_text(f"{setting}:", 300, y_offset, color)
            self.draw_text(f"< {current_value} >", 550, y_offset, color)
            y_offset += 80

    def draw_control_tab(self):
        """Отображение вкладки управления."""
        self.draw_text("В работе", 300, 100)

    def draw_right_block(self):
        """Отображение параметров текущей вкладки."""
        if self.current_tab == 0:
            self.draw_sound_tab()
        elif self.current_tab == 1:
            self.draw_graphics_tab()
        elif self.current_tab == 2:
            self.draw_control_tab()

    def handle_input(self, events):
        """Обработка ввода пользователя."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.left_block_selected:
                    if event.key == pygame.K_UP:
                        self.current_tab = (self.current_tab - 1) % len(self.tabs)
                    elif event.key == pygame.K_DOWN:
                        self.current_tab = (self.current_tab + 1) % len(self.tabs)
                    elif event.key == pygame.K_RETURN:
                        if self.current_tab == len(self.tabs) - 1:  # "Назад"
                            self.open_menu()
                        else:
                            self.left_block_selected = False
                            self.right_block_selected = True
                            self.current_parameter = 0
                    elif event.key == pygame.K_ESCAPE:
                        self.open_menu()

                elif self.right_block_selected:
                    if event.key == pygame.K_UP:
                        self.current_parameter = (self.current_parameter - 1) % len(
                            self.get_current_settings()
                        )
                    elif event.key == pygame.K_DOWN:
                        self.current_parameter = (self.current_parameter + 1) % len(
                            self.get_current_settings()
                        )
                    elif event.key == pygame.K_LEFT:
                        self.adjust_parameter(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_parameter(1)
                    elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        self.left_block_selected = True
                        self.right_block_selected = False

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.current_tab = (self.current_tab - 1) % len(self.tabs)
                elif event.y < 0:
                    self.current_tab = (self.current_tab + 1) % len(self.tabs)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Обработка клика мыши для выбора вкладок."""
        x, y = pos
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(30, 100 + i * 50, 200, 40)
            if tab_rect.collidepoint(x, y):
                self.current_tab = i
                if self.current_tab == len(self.tabs) - 1:  # "Назад"
                    self.open_menu()
                self.left_block_selected = True
                self.right_block_selected = False

    def get_current_settings(self):
        """Получение текущих параметров в зависимости от вкладки."""
        if self.current_tab == 0:
            return list(self.sound_settings.items())
        elif self.current_tab == 1:
            return list(self.graphics_settings.items())
        return []

    def save_and_apply_settings(self):
        """Сохраняем и применяем настройки."""
        if self.current_tab == 0:
            self.apply_settings_callback(self.sound_settings, self.current_graphics_values)
        elif self.current_tab == 1:
            self.apply_settings_callback(self.sound_settings, self.graphics_settings)
        elif self.current_tab == 2:
            self.apply_settings_callback(self.sound_settings, self.graphics_settings)

    def adjust_parameter(self, direction):
        """Изменение значения параметра."""
        if self.current_tab == 0:
            keys = list(self.sound_settings.keys())
            key = keys[self.current_parameter]
            new_value = self.sound_settings[key] + direction * 10
            self.sound_settings[key] = max(0, min(100, new_value))
        elif self.current_tab == 1:
            keys = list(self.graphics_settings.keys())
            key = keys[self.current_parameter]
            options = self.graphics_settings[key]
            current_value = self.current_graphics_values[key]
            new_index = (options.index(current_value) + direction) % len(options)
            self.current_graphics_values[key] = options[new_index]

    def run(self):
        """Запуск настроек."""
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.handle_input(events)
            self.screen.fill((0, 0, 0))  # Очищаем экран
            self.draw_tabs()
            self.draw_right_block()
            pygame.display.flip()
            clock.tick(60)

    def open_menu(self):
        """Открывает экран настроек."""
        if not self.menu:  # Если настройки еще не созданы
            from ui.menu import Menu  # Импортируем класс Menu
            self.menu = Menu(self.screen)  # Создаем объект настроек
        self.menu.run()  # Запускаем экран настроек

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
settings = SettingsPage(screen)
settings.run()
