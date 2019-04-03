import kivy
import sys
sys.setrecursionlimit(100000000)
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
import time
from functools import partial

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '621')
Config.set('graphics', 'resizable', False)


class node:
    def __init__(self, x, y, hori, vert):
        self.x = x
        self.y = y
        self.hori = hori
        self.vert = vert
        self.col = 7


class block:
    def __init__(self, y, x, sz, occ, orient, col):
        self.x = x  # coordinates of upper left corner of rotation area
        self.y = y
        self.sz = sz    # size of rotation grid
        self.occ = occ  # grid squares occupied by block
        self.orient = orient  # orientation of block
        self.col = col


width = 10
height = 20

grid = [[None for x in range(width)] for x in range(height)]
chk = [[0 for x in range(width)] for x in range(height)]


colours = [(0, 1, 1, 1),       # 0 - cyan (long boi)
           (0, 0, 1, 1),       # 1 - blue (J piece)
           (1, 0.647, 0, 1),   # 2 - orange (L piece)
           (1, 1, 0, 1),       # 3 - yellow (square)
           (0, 0.5, 0, 1),     # 4 - green (S piece)
           (1, 0, 0, 1),       # 5 - red (Z piece)
           (0.5, 0, 0.5, 1),   # 6 - purple (T piece)
           (0, 0, 0, 1)]       # 7 - black (empty)

# format: rotates in x by x grid, with [a,b], [c,d] ... blocks coloured
types = [[4, [1, 0], [1, 1], [1, 2], [1, 3]],  # long boi (spawns vertical right)
         [3, [0, 0], [1, 0], [1, 1], [1, 2]],  # J piece (spawns pointy down)
         [3, [1, 0], [1, 1], [1, 2], [0, 2]],  # L piece (spawns pointy down)
         [2, [0, 0], [0, 1], [1, 0], [1, 1]],  # square piece
         [3, [1, 0], [1, 1], [0, 1], [0, 2]],  # S piece (spawns vertical)
         [3, [0, 0], [0, 1], [1, 1], [1, 2]],  # Z piece (spawns vertical)
         [3, [0, 1], [1, 0], [1, 1], [1, 2]]]  # T piece (spawns upside down)


cur = [0]
running = [0]


for i in range(height):
    for j in range(width):
        grid[i][j] = node(j*30+10, i*30+10, 29, 29)


def paintGrid(self):
    self.canvas.clear()
    with self.canvas:
        Color(1,1,1,1)
        Rectangle(pos=(0,0), size=(500, 621))
        Color(.501,.501,.501,1)
        Rectangle(pos=(0, 0), size=(321, 621))
        for i in grid:
            for j in i:
                Color(*colours[j.col])
                Rectangle(pos=(j.x+1, j.y+1), size=(j.hori, j.vert))


def dropBlock(self, *largs):
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = cur[0].col
        if y == 0 or (grid[y-1][x].col != 7 and [i[0]+1, i[1]] not in cur[0].occ):
            '''
            curType = randint(0, 6)
            cur[0] = block(19, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
            dropBlock(self)
            '''
            return
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = 7
    cur[0].y -= 1
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = cur[0].col
    paintGrid(self)
    Clock.schedule_once(partial(dropBlock, self), 0.5)


def runGame(self):
    alive = 1
    score = 0
    probs = [1, 1, 1, 1, 1, 1, 1]   # likelihood of each spawn

    '''
    probability will work as follows: each value in array represents
    how many cycles ago that tetromino was last spawned.
    '''

    curType = randint(0, 6)
    cur[0] = block(19, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
    dropBlock(self)


def shift(val):
    if not cur[0]:
        return
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        x += val
        if x < 0 or x >= 10 or (grid[y][x].col != 7 and [i[0], i[1] + val] not in cur[0].occ):
            return
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = 7
    cur[0].x += val
    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = cur[0].col


def rotate(val):
    if not cur[0]:
        return
    mod = [0, 0]
    occ2 = []

    for i in cur[0].occ:
        if val:
            occ2.append([cur[0].sz-i[1]-1, i[0]])
        else:
            occ2.append([i[1], cur[0].sz-i[0]-1])

    for i in occ2:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        if y < 0 or (grid[y][x].col != 7 and [i[0], i[1]] not in cur[0].occ):
            return

    for i in cur[0].occ:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = 7

    for i in occ2:
        y, x = cur[0].y - i[0], cur[0].x + i[1]
        grid[y][x].col = cur[0].col

    cur[0].occ = occ2


class TetrisGame(Widget):

    def __init__(self, **kwargs):
        super(TetrisGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            rotate(1)
            paintGrid(self)
        elif keycode[1] == 'down':
            rotate(0)
            paintGrid(self)
        elif keycode[1] == 'left':
            shift(-1)
            paintGrid(self)
        elif keycode[1] == 'right':
            shift(1)
            paintGrid(self)
        elif keycode[1] == 'w':
            curType = randint(0, 6)
            cur[0] = block(19, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
            dropBlock(self)
        return True


class MainApp(App):

    def build(self):
        self.title = "Tetris"
        game = TetrisGame()
        paintGrid(game)
        #runGame(game)
        return game


tetris = MainApp()

if __name__ == '__main__':
    tetris.run()
