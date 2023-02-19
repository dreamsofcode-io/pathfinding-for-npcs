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
    def __init__(self, batch, scale, map, assetmanager):
        self._color = 'green'
        self._map = map

        self._animations = {
            NPCState.IDLE: assetmanager.get_animation('npc/green/rifle/idle'),
            NPCState.MOVING: assetmanager.get_animation('npc/green/rifle/move'),
        }

        self._sprite = sprite.Sprite(self._animations[NPCState.IDLE], batch=batch)

        self._base_scale = scale
        self._state = None
        self._scale = scale * 0.4
        self._sprite.scale = self._scale
        self.target = None
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
    def top_left(self):
        return self.position - pmath.Vec2(
            self._sprite.width * self._scale / 2, 
            self._sprite.height * self._scale /2
        )

    @property
    def bottom_right(self):
        return self.position + pmath.Vec2(
            self._sprite.width * self._scale / 2,
            self._sprite.height * self._scale / 2
        )

    @property
    def radius(self):
        return max(self._sprite.width, self._sprite.height) * self._scale / 2

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, angle):
        self._direction = angle
        self._sprite.rotation = math.degrees(angle)

    def place_at(self, pos: pmath.Vec2):
        self._target = None
        self._path = None
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

        if self._target is not None:
            self._path = self._map.find_shortest_path(
                self.position,
                self._target,
            )

            first_idx = self.last_in_line_of_sight()
            if first_idx is not None and first_idx > 0:
                self._path = self._path[first_idx:]

    def in_line_of_sight(self, pos: pmath.Vec2):
        if pos is None:
            return False
        return self._map.is_lineofsight(self.position, pos, padding=self.radius)
    
    def target_in_line_of_sight(self):
        return self.in_line_of_sight(self._target)

    def last_in_line_of_sight(self):
        if self._path is None:
            return None

        last_idx = None

        for idx, pos in enumerate(self._path):
            if self.in_line_of_sight(pos):
                last_idx = idx

        return last_idx
    
    def update(self, dt):
        if self._path is not None:
            self.state = NPCState.MOVING

            # Face towards the next path point
            self.turn_towards_target(dt, self._path[0])

            # Move towards the next path point
            if self.move_towards_target(dt, self._path[0]):
                self._path.pop(0)
            if len(self._path) == 0:
                self._path = None

        elif self.target_in_line_of_sight():
            self.state = NPCState.MOVING

            self.turn_towards_target(dt, self._target)
            if self.move_towards_target(dt, self._target):
                self._target = None 
                self._path = None
        else:
            self.state = NPCState.IDLE

    def move_towards_target(self, dt, target) -> bool:
        # If target doesn't exist. Do nothing
        if target is None:
            return True

        # If we are already at the target, no need to move
        if self.position == target:
            return True

        # Calculate the velocity this frame
        speed = 125 * dt * self._base_scale

        # Calculate the angle to the target
        target_angle = math.atan2(
            target.y - self.position.y, 
            target.x - self.position.x
        )

        # Calculate the velocity vector
        self._velocity.x = math.cos(target_angle) * speed
        self._velocity.y = math.sin(target_angle) * speed

        position = self.position + self._velocity

        # If we are close enough to the target, snap to it
        if math.fabs(position.x - target.x) < speed:
            position.x = target.x
        if math.fabs(position.y - target.y) < speed:
            position.y = target.y

        self.position = position

        return False
        
    def turn_towards_target(self, dt, target):
        # If we have no target, no need to turn
        if target is None:
            return
        
        # Calculate the angle to the target
        target_dir = math.atan2(
            self.position.y - target.y,
            target.x - self.position.x,
        )

        # If we are already facing the target, no need to turn 
        if target_dir == self.direction:
            return

        # Calculate the amount of degrees we can turn this frame
        turn_speed = 18 * dt

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
