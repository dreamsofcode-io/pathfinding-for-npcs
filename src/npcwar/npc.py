from pyglet import math as pmath
import math
from pyglet import shapes
from pyglet import graphics
from pyglet import sprite
import pyglet
from enum import Enum

class NPCState(Enum):
    IDLE = 0
    MOVING = 1

class NPC:
    def __init__(self, batch, scale, assetmanager):
        self._color = 'green'

        self._animations = {
            NPCState.IDLE: assetmanager.get_animation('npc/green/rifle/idle'),
            NPCState.MOVING: assetmanager.get_animation('npc/green/rifle/move'),
        }

        self._sprite = sprite.Sprite(self._animations[NPCState.IDLE], batch=batch)

        self._scale = scale * 0.25
        self._sprite.scale = self._scale
        self.target = pmath.Vec2(0,0)
        self.direction = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: NPCState):
        self._state = state
        self._sprite.image = self._animations[state]

    @property
    def position(self):
        return pmath.Vec2(self._sprite.x, self._sprite.y)

    @position.setter
    def position(self, pos: pmath.Vec2):
        self._sprite.x = pos.x
        self._sprite.y = pos.y

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, angle):
        self._direction = angle
        self._sprite.rotation = math.degrees(angle)

    def place_at(self, pos: pmath.Vec2):
        self._target = None
        self._direction = 0
        self.position = pos
        self._velocity = pmath.Vec2(0,0)
        self.is_aiming = False
        self.cooldown_timer = 0
        self.respawn_timer = 0
        self.is_firing = False
        self.accuracy = 0
        self.last_accuracy = 1
        self.health = 100

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, pos: pmath.Vec2):
        self._target = pos

    def update(self, dt):
        turn_speed = 25 * dt

        if self._target is not None:
            current_direction = self.direction

            target_dir = math.atan2(self.position.y - self._target.y, self._target.x - self.position.x)
            if target_dir != current_direction:
                if target_dir > current_direction:
                    if target_dir - current_direction > math.pi:
                        self.direction -= turn_speed
                    else:
                        self.direction += turn_speed
                else:
                    if current_direction - target_dir > math.pi:
                        self.direction += turn_speed
                    else:
                        self.direction -= turn_speed

                if self.direction > math.pi:
                    self.direction -= math.pi * 2
                elif self.direction < -math.pi:
                   self.direction += math.pi * 2


                if math.fabs(self.direction - target_dir) < turn_speed:
                    self.direction = target_dir
