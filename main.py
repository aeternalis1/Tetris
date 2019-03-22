import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock

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
        self.col = 0


class block:
    def __init__(self, x, y, t, orient):
        self.x = x  # coordinates of upper left corner of rotation area
        self.y = y
        self.t = t  # type of block
        self.orient = orient  # orientation of block


width = 10
height = 20

grid = [[None for x in range(width)] for x in range(height)]
chk = [[0 for x in range(width)] for x in range(height)]


colours = [(0, 0, 0, 1),       # 0 - black (empty)
           (0, 1, 1, 1),       # 1 - cyan (long boi)
           (0, 0, 1, 1),       # 2 - blue (J piece)
           (1, 0.647, 0, 1),   # 3 - orange (L piece)
           (1, 1, 0, 1),       # 4 - yellow (square)
           (0, 0.5, 1, 1),     # 5 - green (S piece)
           (1, 0, 0, 1),       # 6 - red (Z piece)
           (0.5, 0, 0.5, 1)]   # 7 - purple (T piece)

# format: rotates in x by x grid, with [a,b], [c,d] ... blocks coloured
types = [[4, 4, [0, 2], [1, 2], [2, 2], [2, 3]],  # long boi (spawns vertical right)
         [3, 3, [0, 3], [0, 2], [1, 2], [2, 2]],  # J piece (spawns pointy down)
         [3, 3, [0, 1], [0, 2], [1, 2], [2, 2]],  # L piece (spawns pointy down)
         [2, 2, [0, 0], [0, 1], [1, 0], [1, 1]],  # square piece
         [3, 3, [0, 1], [1, 1], [1, 2], [2, 2]],  # S piece (spawns vertical)
         [3, 3, [0, 2], [1, 2], [1, 1], [2, 1]],  # Z piece (spawns vertical)
         [3, 3, [0, 1], [1, 0], [1, 1], [1, 2]]]  # T piece (spawns upside down)


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


class MainApp(App):
    def build(self):
        self.title = "Tetris"
        parent = Widget()
        paintGrid(parent)
        return parent
    def runGame(self):
        alive = 1
        score = 0
        while alive:
            pass


tetris = MainApp()

if __name__ == '__main__':
    tetris.run()
