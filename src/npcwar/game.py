import pyglet
from pyglet import math
from npcwar import map, npc, marker, assets, rectangle, graph

class Game:
    def __init__(self, width, height, scale):
        self.assetmanager = assets.AssetManager()
        self.batch = pyglet.graphics.Batch()

        self._graph = graph.setup_graph(scale)

        self.map = map.Map(width=width, height=height, scale=scale, graph=self._graph)
        self.map.add_block(149, 540, 200, 90)
        self.map.add_block(348, 144, 90, 486)
        self.map.add_block(438, 372, 429, 90)
        self.map.add_block(754, 585, 270, 90)
        self.map.add_block(597, 144, 427, 90)

        self.map.add_spawn_point(64, 368, 'green')

        self.npc = npc.NPC(
            batch=self.batch, scale=scale, assetmanager=self.assetmanager, map=self.map
        )

        self.npc.place_at(self.map.get_spawn_point('green'))
        self.marker = marker.Marker(batch=self.batch, scale=scale, map=self.map)

        pyglet.clock.schedule(self.update, 1/60.0)


    def draw(self):
        self.map.draw()
        self.batch.draw()

    def is_valid_marker_position(self, x, y):
        return not self.map.check_collision(math.Vec2(x, y), padding=self.npc.radius)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            print(x // 2, y // 2)
            if self.marker.check_collision(math.Vec2(x, y)):
                self.marker.remove_marker()
                self.npc.target = None
            elif self.is_valid_marker_position(x, y):
                self.marker.place_at(math.Vec2(x, y))
                self.npc.target = math.Vec2(x, y)

        if button == pyglet.window.mouse.RIGHT:
            self.marker.remove_marker()
            self.npc.target = None

    def update(self, dt, args):
        self.npc.update(dt)
        if self.npc.target is None:
            self.marker.remove_marker()

