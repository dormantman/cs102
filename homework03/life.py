import copy
import pathlib
import random
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [
            [
                random.choice([0, 1]) if randomize else 0
                for _ in range(self.cols)
            ] for _ in range(self.rows)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j

                if i == 0 and j == 0:
                    continue

                if 0 <= w < self.cols and 0 <= h < self.rows:
                    neighbours.append(self.curr_generation[h][w])

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.curr_generation)

        for h in range(self.rows):
            for w in range(self.cols):
                neighbours = self.get_neighbours((h, w))
                alive_neighbours = sum(neighbours)

                if alive_neighbours != 2 and alive_neighbours != 3:
                    new_grid[h][w] = 0

                elif alive_neighbours == 3:
                    new_grid[h][w] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.generations += 1
        self.prev_generation, self.curr_generation = self.curr_generation, self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """

        # from pprint import pprint
        # pprint(self.prev_generation)
        # pprint(self.curr_generation)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.prev_generation[row][col] != self.curr_generation[row][col]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """

        with filename.open() as file:
            grid = [list(map(int, col.strip())) for col in file.readlines()]

        size = len(grid), len(grid[0])

        new_game = GameOfLife(size, randomize=False)
        new_game.curr_generation = grid
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        grid_txt = '\n'.join([''.join(map(str, col)) for col in self.curr_generation])

        with filename.open(mode='w') as file:
            file.write(grid_txt)


#
# class GameOfLife:
#     def __init__(self, width=640, height=480, cell_size=10, speed=10):
#         self.width = width
#         self.height = height
#         self.cell_size = cell_size
#
#         # Устанавливаем размер окна
#         self.screen_size = width, height
#         # Создание нового окна
#         self.screen = pygame.display.set_mode(self.screen_size)
#
#         # Вычисляем количество ячеек по вертикали и горизонтали
#         self.cell_width = self.width // self.cell_size
#         self.cell_height = self.height // self.cell_size
#
#         # Скорость протекания игры
#         self.speed = speed
#
#     def draw_grid(self):
#         """ Отрисовать сетку """
#         for x in range(0, self.width, self.cell_size):
#             pygame.draw.line(self.screen, pygame.Color('black'),
#                              (x, 0), (x, self.height))
#         for y in range(0, self.height, self.cell_size):
#             pygame.draw.line(self.screen, pygame.Color('black'),
#                              (0, y), (self.width, y))
#
#     def run(self):
#         """ Запустить игру """
#         pygame.init()
#         clock = pygame.time.Clock()
#         pygame.display.set_caption('Game of Life')
#         self.screen.fill(pygame.Color('white'))
#
#         # Создание списка клеток
#         self.clist = self.cell_list(randomize=True)
#
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     running = False
#             self.draw_grid()
#
#             # Отрисовка списка клеток
#             self.draw_cell_list(self.clist)
#             # Выполнение одного шага игры (обновление состояния ячеек)
#             self.clist = self.update_cell_list(self.clist)
#
#             pygame.display.flip()
#             clock.tick(self.speed)
#         pygame.quit()
#
#     def cell_list(self, randomize=True) -> List[List[int]]:
#         """ Создание списка клеток.
#
#         :param randomize: Если True, то создается список клеток, где
#         каждая клетка равновероятно может быть живой (1) или мертвой (0).
#         :return: Список клеток, представленный в виде матрицы
#         """
#         clist = []
#         for h in range(self.height // self.cell_size):
#             row = []
#             for w in range(self.width // self.cell_size):
#                 if randomize:
#                     row.append(random.randint(0, 1))
#                 if not randomize:
#                     row.append(0)
#             clist.append(row)
#         return clist
#
#     def draw_cell_list(self, clist: List[List[int]]) -> None:
#         """ Отображение списка клеток
#
#         :param rects: Список клеток для отрисовки, представленный в виде матрицы
#         """
#         white = pygame.Color('white')
#         green = pygame.Color('green')
#         for h in range(len(clist)):
#             for w in range(len(clist[h])):
#                 y = h * self.cell_size
#                 x = w * self.cell_size
#                 if clist[h][w] == 0:
#                     pygame.draw.rect(self.screen, white, [x, y, self.cell_size, self.cell_size])
#                 else:
#                     pygame.draw.rect(self.screen, green, [x, y, self.cell_size, self.cell_size])
#         pass
#
#     def get_neighbours(self, cell: Tuple[int, int]) -> List:
#         """ Вернуть список соседей для указанной ячейки
#
#         :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
#         :return: Одномерный список ячеек, смежных к ячейке cell
#         """
#         neighbours = []
#         for i in range(-1, 2):
#             for j in range(-1, 2):
#                 h = cell[0] + i
#                 w = cell[1] + j
#                 if i == 0 and j == 0:
#                     continue
#                 if 0 <= w < self.cell_width and 0 <= h < self.cell_height:
#                     neighbours.append(self.clist[h][w])
#         return neighbours
#
#     def update_cell_list(self, cell_list: List) -> List:
#         """ Выполнить один шаг игры.
#
#         Обновление всех ячеек происходит одновременно. Функция возвращает
#         новое игровое поле.
#
#         :param cell_list: Игровое поле, представленное в виде матрицы
#         :return: Обновленное игровое поле
#         """
#         new_clist = copy.deepcopy(cell_list)
#         for h in range(self.cell_height):
#             for w in range(self.cell_width):
#                 neighbours = self.get_neighbours((h, w))
#                 alive_neighbours = sum(neighbours)
#                 if alive_neighbours != 2 and alive_neighbours != 3:
#                     new_clist[h][w] = 0
#                 elif alive_neighbours == 3:
#                     new_clist[h][w] = 1
#         return new_clist


if __name__ == '__main__':
    game = GameOfLife()
    game.run()
