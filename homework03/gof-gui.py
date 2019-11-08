import argparse

from life import GameOfLife
from life_gui import GUI

parser = argparse.ArgumentParser(description='Game of life')
parser.add_argument('--rows', default=24, type=int, nargs='?', help='Number of rows')
parser.add_argument('--cols', default=80, type=int, nargs='?', help='Number of cols')
parser.add_argument('--max-generations', default=50, type=int, nargs='?', help='Number of max generations')
parser.add_argument('--width', default=320, type=int, nargs='?', help='Screen width')
parser.add_argument('--height', default=240, type=int, nargs='?', help='Screen height')
parser.add_argument('--cell-size', default=20, type=int, nargs='?', help='Cell size')
parser.add_argument('--speed', default=10, type=int, nargs='?', help='Game speed')

args = parser.parse_args()

life = GameOfLife((args.rows, args.cols), max_generations=args.max_generations)

ui = GUI(life, args.width, args.height, args.cell_size, args.speed)
ui.run()
