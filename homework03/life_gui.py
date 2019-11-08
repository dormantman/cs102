import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, width: int = 640, height: int = 480, cell_size: int = 10,
                 speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        super().__init__(life)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        white = pygame.Color('white')
        green = pygame.Color('green')

        grid = self.life.curr_generation

        for h in range(self.cell_height):
            for w in range(self.cell_width):
                y = h * self.cell_size
                x = w * self.cell_size

                color = white if grid[h][w] == 0 else green
                pygame.draw.rect(self.screen, color, [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1])

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.life.curr_generation = self.life.create_grid(randomize=True)

        pause = True

        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        grid = self.life.curr_generation
                        w, h = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size
                        grid[h][w] = 0 if grid[h - 1][w - 1] else 1

                    elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                        pause = not pause

                    elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        running = False

                self.draw_lines()

                # Отрисовка списка клеток
                self.draw_grid()
                # Выполнение одного шага игры (обновление состояния ячеек)
                if not pause:
                    self.life.step()

                pygame.display.update()
                pygame.display.flip()
                clock.tick(self.speed)

            except KeyboardInterrupt:
                running = False

        pygame.quit()


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)

    ui = GUI(life, cell_size=20)
    ui.run()
