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
types = [[4, [0, 2], [1, 2], [2, 2], [3, 2]],  # long boi (spawns vertical right)
         [3, [0, 3], [0, 2], [1, 2], [2, 2]],  # J piece (spawns pointy down)
         [3, [0, 1], [0, 2], [1, 2], [2, 2]],  # L piece (spawns pointy down)
         [2, [0, 0], [0, 1], [1, 0], [1, 1]],  # square piece
         [3, [0, 1], [1, 1], [1, 2], [2, 2]],  # S piece (spawns vertical)
         [3, [0, 2], [1, 2], [1, 1], [2, 1]],  # Z piece (spawns vertical)
         [3, [0, 1], [1, 0], [1, 1], [1, 2]]]  # T piece (spawns upside down)


cur = [0]
running = [0]


for i in range(height):
    for j in range(width):
        grid[i][j] = node(j*30+10, i*30+10, 29, 29)


def paintGrid(self):
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
        if y == 0 or (grid[y-1][x].col != 7 and [abs(y-cur[0].y-1), x-cur[0].x] not in cur[0].occ):
            curType = randint(0, 6)
            cur[0] = block(19, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
            dropBlock(self)
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


class MainApp(App):

    def build(self):
        self.title = "Tetris"
        parent = Widget()
        paintGrid(parent)
        runGame(parent)
        return parent


tetris = MainApp()

if __name__ == '__main__':
    tetris.run()
