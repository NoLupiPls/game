class GameState:
    """Базовый класс для состояний игры."""
    def __init__(self, game):
        self.game = game  # Ссылка на основной объект игры
        self.running = True  # Определяет, активно ли состояние

    def handle_events(self, events):
        """Обработка событий."""
        pass

    def update(self, dt):
        """Обновление логики."""
        pass

    def draw(self, screen):
        """Отрисовка состояния."""
        pass

    def enter_state(self):
        """Действия при входе в состояние."""
        pass

    def exit_state(self):
        """Действия при выходе из состояния."""
        pass


class MainMenuState(GameState):
    """Состояние главного меню."""
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Start Game", "Options", "Exit"]
        self.selected_option = 0

    def handle_events(self, events):
        for event in events:
            if event.type == self.game.pygame.KEYDOWN:
                if event.key == self.game.pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == self.game.pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == self.game.pygame.K_RETURN:
                    self.execute_option()

    def execute_option(self):
        if self.selected_option == 0:  # Start Game
            self.game.change_state(GameplayState(self.game))
        elif self.selected_option == 1:  # Options
            self.game.change_state(OptionsState(self.game))
        elif self.selected_option == 2:  # Exit
            self.game.running = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        font = self.game.pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (100, 100 + i * 40))


class GameplayState(GameState):
    """Состояние игрового процесса."""
    def __init__(self, game):
        super().__init__(game)
        self.level = None  # Уровень игры

    def handle_events(self, events):
        for event in events:
            if event.type == self.game.pygame.KEYDOWN:
                if event.key == self.game.pygame.K_ESCAPE:
                    self.game.change_state(PauseState(self.game))

    def update(self, dt):
        if self.level:
            self.level.update(dt)

    def draw(self, screen):
        if self.level:
            self.level.draw(screen)


class PauseState(GameState):
    """Состояние паузы."""
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        for event in events:
            if event.type == self.game.pygame.KEYDOWN:
                if event.key == self.game.pygame.K_ESCAPE:
                    self.running = False

    def draw(self, screen):
        screen.fill((50, 50, 50))
        font = self.game.pygame.font.Font(None, 48)
        text_surface = font.render("Paused", True, (255, 255, 255))
        screen.blit(text_surface, (200, 200))


class OptionsState(GameState):
    """Состояние настроек."""
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        for event in events:
            if event.type == self.game.pygame.KEYDOWN:
                if event.key == self.game.pygame.K_ESCAPE:
                    self.running = False

    def draw(self, screen):
        screen.fill((50, 50, 50))
        font = self.game.pygame.font.Font(None, 36)
        text_surface = font.render("Options Menu (Press ESC to go back)", True, (255, 255, 255))
        screen.blit(text_surface, (50, 200))
        