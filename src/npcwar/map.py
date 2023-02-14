from pyglet import math as pmath
import pyglet
import math

class Map:
    def __init__(self, width, height, scale):
        tile_size = 32 * scale
        self.width = width
        self.height = height
        self.scale = scale
        self._batch = pyglet.graphics.Batch()
        self.rect = pyglet.shapes.Rectangle(0, 0, width , height, color=(69, 71, 90), batch=self._batch)

    def is_lineofsight(self, a: pmath.Vec2, b: pmath.Vec2) -> bool:
        True

    def draw(self):
        self._batch.draw()

