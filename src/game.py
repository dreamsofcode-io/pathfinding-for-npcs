import pyglet
from pyglet import math
import map
import npc
import marker

class Game:
    def __init__(self, width, height):
        self.map = map.Map(width=width, height=height)
        self.batch = pyglet.graphics.Batch()
        self.npc = npc.NPC(batch=self.batch)
        self.npc.place_at(math.Vec2(width // 2, height // 2))
        self.marker = marker.Marker(batch=self.batch)

    def draw(self):
        self.map.draw()
        self.batch.draw()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.marker.check_collision(math.Vec2(x, y)):
                self.marker.remove_marker()
            else:
                self.marker.place_at(math.Vec2(x, y))

        if button == pyglet.window.mouse.RIGHT:
            self.marker.remove_marker()

    def update():
        pass

