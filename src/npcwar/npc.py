from pyglet import math
from pyglet import shapes
from pyglet import graphics
from pyglet import sprite
from enum import Enum

class NPCState(Enum):
    IDLE = 0
    MOVING = 1

class NPC:
    def __init__(self, batch, scale, assetmanager):
        self._color = 'green'

        self._animations = {
            NPCState.IDLE: assetmanager.get_animation('npc/green/rifle/idle'),
        }

        self._sprite = sprite.Sprite(self._animations[NPCState.IDLE], batch=batch)

        self._scale = scale * 0.25
        self._sprite.scale = self._scale
        self._direction = 0

    @property
    def position(self):
        return self.circle.position

    @position.setter
    def position(self, pos: math.Vec2):
        self._sprite.x = pos.x
        self._sprite.y = pos.y

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
