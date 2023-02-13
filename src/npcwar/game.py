import pyglet
from pyglet import math
from npcwar import map, npc, marker, assets

class Game:
    def __init__(self, width, height, scale):
        self.assetmanager = assets.AssetManager()
        self.batch = pyglet.graphics.Batch()
        self.map = map.Map(width=width, height=height, scale=scale, asset_manager=self.assetmanager)
        self.npc = npc.NPC(batch=self.batch, scale=scale, assetmanager=self.assetmanager)
        self.npc.place_at(math.Vec2(width // 2, height // 2))
        self.marker = marker.Marker(batch=self.batch, scale=scale)
        pyglet.clock.schedule(self.update, 1/60.0)

    def draw(self):
        #self.map.draw()
        self.batch.draw()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.marker.check_collision(math.Vec2(x, y)):
                self.marker.remove_marker()
                self.npc.target = None
            else:
                self.marker.place_at(math.Vec2(x, y))
                self.npc.target = math.Vec2(x, y)

        if button == pyglet.window.mouse.RIGHT:
            self.marker.remove_marker()
            self.npc.target = None

    def update(self, dt, args):
        self.npc.update(dt)

