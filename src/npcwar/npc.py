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

        self._state = None
        self._scale = scale * 0.25
        self._sprite.scale = self._scale
        self.target = pmath.Vec2(0,0)
        self.direction = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: NPCState):
        if self._state == state:
            return
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
        if self._target is not None:
            self.state = NPCState.MOVING
            self.turn_towards_target(dt)
            self.move_towards_target(dt)
        else:
            self.state = NPCState.IDLE

    def move_towards_target(self, dt):
        # If target doesn't exist. Do nothing
        if self.target is None:
            return

        # If we are already at the target, no need to move
        if self.position == self.target:
            self.target = None
            return

        # Calculate the velocity this frame
        speed = 200 * dt

        # Calculate the angle to the target
        target_angle = math.atan2(
            self.target.y - self.position.y, 
            self.target.x - self.position.x
        )

        # Calculate the velocity vector
        self._velocity.x = math.cos(target_angle) * speed
        self._velocity.y = math.sin(target_angle) * speed

        position = self.position + self._velocity

        # If we are close enough to the target, snap to it
        if math.fabs(position.x - self.target.x) < speed:
            position.x = self.target.x
        if math.fabs(position.y - self.target.y) < speed:
            position.y = self.target.y

        self.position = position
        
    def turn_towards_target(self, dt):
        # If we have no target, no need to turn
        if self._target is None:
            return
        
        # Calculate the angle to the target
        target_dir = math.atan2(
            self.position.y - self._target.y,
            self._target.x - self.position.x,
        )

        # If we are already facing the target, no need to turn 
        if target_dir == self.direction:
            return

        # Calculate the amount of degrees we can turn this frame
        turn_speed = 25 * dt

        # Turn towards the target
        if target_dir > self.direction:
            # If the target is on the other side of the circle, turn the other way
            if target_dir - self.direction > math.pi:
                self.direction -= turn_speed
            else:
                self.direction += turn_speed
        else:
            # If the target is on the other side of the circle, turn the other way
            if self.direction - target_dir > math.pi:
                self.direction += turn_speed
            else:
                self.direction -= turn_speed

        # Make sure we don't turn too far
        if self.direction > math.pi:
            self.direction -= math.pi * 2
        elif self.direction < -math.pi:
            self.direction += math.pi * 2

        # If we are close enough to the target, just face it to avoid jittering
        if math.fabs(self.direction - target_dir) < turn_speed:
            self.direction = target_dir
