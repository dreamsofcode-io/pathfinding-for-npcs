import pyglet
from pyglet import shapes
from pyglet import math

class Marker:
    def __init__(self, batch, scale):
        self._active = False
        self._img = pyglet.image.load('./assets/images/location.png')
        self._img.anchor_x = self._img.width // 2
        self._img.anchor_y = 5
        self._sprite = pyglet.sprite.Sprite(self._img, batch=batch)
        self._sprite.visible = False
        self._sprite.scale = scale * 0.5

    def place_at(self, pos: math.Vec2):
        self._sprite.visible = True
        self._sprite.x = pos.x
        self._sprite.y = pos.y

    def remove_marker(self):
        self._sprite.visible = False

    def check_collision(self, pos: math.Vec2):
        if self._sprite.visible:
            left = self._sprite.x - self._img.width // 2
            right = self._sprite.x + self._img.width // 2
            if pos.x > left and pos.x < right:
                return pos.y > self._sprite.y and pos.y < self._sprite.y + self._img.height
        else:
            return False
