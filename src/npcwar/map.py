from pyglet import math as pmath
import pyglet
from shapely.geometry import LineString
import math
from npcwar import rectangle, graph

class Map:
    def __init__(self, width, height, scale, graph, show_graph):
        self._graph = graph
        self.width = width
        self.height = height
        self.scale = scale
        self._batch = pyglet.graphics.Batch()
        self._edge_group = pyglet.graphics.Group(0)
        self._node_group = pyglet.graphics.Group(1)
        self._text_group = pyglet.graphics.Group(2)
        self.rect = pyglet.shapes.Rectangle(0, 0, width , height, color=(108, 112, 134), batch=self._batch)
        self._blocks = []
        self._nodes = []
        self._nodetext = []
        self._edges = []
        self._spawn_points = {}
        if show_graph:
            self.add_graph()

    def is_lineofsight(self, a: pmath.Vec2, b: pmath.Vec2, padding: int = 0) -> bool:
        line = LineString([(a.x, a.y), (b.x, b.y)])
        for block in self._blocks:
            poly = LineString(
                [
                    (block.x, block.y),
                    (block.x + block.width, block.y),
                    (block.x + block.width, block.y + block.height),
                    (block.x, block.y + block.height)
                ]
            )
            if line.intersects(poly):
                return False
        
        return True

    def add_block(self, x: int, y: int, width: int, height: int):
        r = pyglet.shapes.Rectangle(
            x * self.scale, 
            y * self.scale,
            width * self.scale,
            height * self.scale,
            color=(244, 244, 244),
            batch=self._batch,
        )

        self._blocks.append(r)

    def add_graph(self):
        for node in self._graph.nodes():
            self._nodes.append(pyglet.shapes.Circle(
                node.x,
                node.y,
                15 * self.scale,
                color=(249, 226, 175),
                batch=self._batch,
                group=self._node_group,
            ))

            self._nodetext.append(pyglet.text.Label(
                str(node.name),
                font_name='Arial',
                font_size=20,
                x=node.x,
                y=node.y,
                anchor_x='center',
                anchor_y='center',
                color=(0, 0, 0, 255),
                batch=self._batch,
                group=self._text_group,
            ))
    
            for neighbour in node.neighbours:
                self._edges.append(pyglet.shapes.Line(
                    node.x,
                    node.y,
                    neighbour.x,
                    neighbour.y,
                    width=3 * self.scale,
                    color=(148, 226, 213),
                    batch=self._batch,
                    group=self._edge_group
                ))

    def find_shortest_path(self, start, end):
        start_node = self.find_closest_node(start)
        end_node = self.find_closest_node(end)
        return self._graph.find_shortest_path(start_node, end_node)

    def find_closest_node(self, point: pmath.Vec2) -> graph.Node:
        closest_node = None
        closest_distance = math.inf
        for node in self._graph.nodes():
            distance = math.sqrt((node.x - point.x) ** 2 + (node.y - point.y) ** 2)
            if distance < closest_distance:
                closest_node = node
                closest_distance = distance

        return closest_node

    def add_spawn_point(self, x: int, y: int, team: str):
        self._spawn_points[team] = pmath.Vec2(x * self.scale, y * self.scale)

    def get_spawn_point(self, team: str):
        return self._spawn_points[team]
        
    def add_rect(self, rect: rectangle.Rectangle2D):
        self.add_block(rect.x, rect.y, rect.width, rect.height)

    def draw(self):
        self._batch.draw()

    def check_collision(self, point: pmath.Vec2, padding: int = 0) -> bool:
        padding = padding // 2
        for block in self._blocks:
            if block.x - padding < point.x < block.x + block.width + padding and block.y - padding < point.y < block.y + block.height + padding:
                return True
        return False

