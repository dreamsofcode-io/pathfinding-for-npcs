from pyglet import math

class Map:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale

    def is_lineofsight(self, a: math.Vec2, b: math.Vec2) -> bool:
        True

    def draw(self):
        pass
