import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)


class node:
    def __init__(self, x, y, hori, vert):
        self.x = x
        self.y = y
        self.hori = hori
        self.vert = vert
        self.col = 0


width = 10
height = 20

grid = [[None for x in range(width)] for x in range(height)]
chk = [[0 for x in range(width)] for x in range(height)]


colours = [(0,0,0,1),(0,1,0,1),(1,0,0,1),(1,1,1,1)]


for i in range(height):
    for j in range(width):
        grid[i][j] = node(j*30+50, i*30+50, 29, 29)


def paintGrid(self):
    with self.canvas:
        Color(*colours[3])
        Rectangle(pos=(0,0), size=(700, 800))
        Color(.501,.501,.501,1)
        Rectangle(pos=(40, 40), size=(321, 621))
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


tetris = MainApp()

if __name__ == '__main__':
    tetris.run()