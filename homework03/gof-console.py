import argparse

from life import GameOfLife
from life_console import Console

parser = argparse.ArgumentParser(description='Game of life')
parser.add_argument('--rows', default=24, type=int, nargs='?', help='Number of rows')
parser.add_argument('--cols', default=80, type=int, nargs='?', help='Number of cols')
parser.add_argument('--max-generations', default=50, type=int, nargs='?', help='Number of max generations')

args = parser.parse_args()

life = GameOfLife((args.rows, args.cols), max_generations=args.max_generations)

ui = Console(life)
ui.run()
