from pyglet import math as pmath
import pyglet
import math


class Map:
    def __init__(self, width, height, scale, asset_manager):
        tile_size = 32 * scale
        self.width = width
        self.height = height
        self.scale = scale
   
    def is_lineofsight(self, a: pmath.Vec2, b: pmath.Vec2) -> bool:
        True

    def draw(self):
        pass

