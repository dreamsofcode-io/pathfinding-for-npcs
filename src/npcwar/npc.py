from pyglet import math
from pyglet import shapes
from pyglet import graphics

class NPC:
    def __init__(self, batch, scale):
        self.color = color=(255, 0, 0)
        self._scale = scale
        self._circle = shapes.Circle(x=0, y=0, radius=10 * scale, color=self.color, batch=batch)
        self._line = shapes.Line(x=0, y=0, x2=0, y2=0, width=4 * scale, color=self.color, batch=batch)
        self._direction = 0

    @property
    def position(self):
        return self.circle.position

    @position.setter
    def position(self, pos: math.Vec2):
        self._circle.position = pos
        self._line.position = pos
        pointer = math.Vec2.from_polar(13 * self._scale, self._direction) + pos
        self._line.x2 = pointer.x
        self._line.y2 = pointer.y

    def place_at(self, pos: math.Vec2):
        self._direction = 0
        self.position = pos
        self._velocity = math.Vec2(0,0)
        self.is_aiming = False
        self.cooldown_timer = 0
        self.respawn_timer = 0
        self.is_firing = False
        self.accuracy = 0
        self.last_accuracy = 1
        self.health = 100

    def update(self, dt):
        pass
