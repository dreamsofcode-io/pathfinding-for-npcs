import pyglet
from pyglet import math
from npcwar import map, npc, marker, assets

class Game:
    def __init__(self, width, height, scale):
        self.map = map.Map(width=width * scale, height=height * scale, scale=scale)
        self.batch = pyglet.graphics.Batch()
        self.assetmanager = assets.AssetManager()
        self.npc = npc.NPC(batch=self.batch, scale=scale, assetmanager=self.assetmanager)
        self.npc.place_at(math.Vec2(width // 2, height // 2))
        self.marker = marker.Marker(batch=self.batch, scale=scale)

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

