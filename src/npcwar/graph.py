from npcwar import util
from pyglet import math
import math as m

class Graph:
    def __init__(self, nodes, scale):
        self._scale = scale
        self._nodes = []
        self._nodemap = {}

        for node in nodes:
            node.x *= scale
            node.y *= scale
            self._nodes.append(node)
            self._nodemap[node.name] = node

    def nodes(self):
        return self._nodes

    def add_node(self, node):
        if node not in self.__graph_dict:
            self._nodemap[node.name] = []

    def add_edge(self, node, neighbour):
        if node in self._nodemap and neighbour in self._nodemap:
            self._nodemap[node].add_neighbour(self._nodemap[neighbour])
            self._nodemap[neighbour].add_neighbour(self._nodemap[node])

    def calculate_distances(self):
        for node in self._nodes:
            node.calc_distances()

    def get_node(self, name):
        return self._nodemap[name]

    def get_distance(self, a, b):
        node_a = self.get_node(a)
        node_b = self.get_node(b)
        pos_a = math.Vec2(node_a.x, node_a.y)
        pos_b = math.Vec2(node_b.x, node_b.y)
        return util.calculate_distance(pos_a, pos_b)

    def find_closest_node(self, pos):
        closest_node = None
        closest_distance = m.inf

        for node in self._nodes:
            node_pos = math.Vec2(node.x, node.y)

            if not self.is_lineofsight(pos, node_pos):
                continue

            distance = util.calculate_distance(pos, node_pos)

            if distance < closest_distance:
                closest_node = node
                closest_distance = distance

        return closest_node

    def find_lowest_cost(self, costs, visited):
        lowest_cost = m.inf
        lowest_cost_node = None

        for node in self._nodes:
            cost = costs[node.name]

            if cost < lowest_cost and node.name not in visited:
                lowest_cost = cost
                lowest_cost_node = node

        return lowest_cost_node

    def find_shortest_path(self, start_node, end_node):
        costs = {}

        # Set all costs to infinity
        for node in self._nodes:
            costs[node.name] = m.inf

        # Set the cost of the start node to 0 and set as current node
        current_node = start_node
        costs[start_node.name] = 0

        visited = []
        parents = {}

        # Loop until we reach the end node
        while current_node.name != end_node.name:
            for neighbour in current_node.neighbours:

                if neighbour.name in visited:
                    continue

                if neighbour.name == end_node.name:
                    parents[neighbour.name] = current_node.name
                    current_node = end_node
                    break

                distance = current_node.get_distance(neighbour.name)
                heuristic = self.get_distance(neighbour.name, end_node.name)
                new_cost = costs[current_node.name] + distance + heuristic

                if new_cost < costs[neighbour.name]:
                    costs[neighbour.name] = new_cost
                    parents[neighbour.name] = current_node.name

            if current_node.name == end_node.name:
                break

            visited.append(current_node.name)
            current_node = self.find_lowest_cost(costs, visited)

        nodepath = [end_node]
        
        # Reconstruct the path from the parents
        while nodepath[0].name != start_node.name:
            nodepath.insert(0, self.get_node(parents[nodepath[0].name]))

        # Convert the path to a list of positions
        path = []
        for node in nodepath:
            path.append(math.Vec2(node.x, node.y))

        return path

class Node:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.neighbours = []
        self.distances = {}

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        
    def get_distance(self, neighbour):
        return self.distances[neighbour]

    def calc_distances(self):
        for neighbour in self.neighbours:
            pos1 = math.Vec2(self.x, self.y)
            pos2 = math.Vec2(neighbour.x, neighbour.y)
            distance = util.calculate_distance(pos1, pos2)

            self.distances[neighbour.name] = distance

def setup_graph(scale):
    nodes = [
        Node('a', 240, 715),
        Node('b', 240, 410),
        Node('c', 240, 50),
        Node('d', 525, 50),
        Node('e', 525, 295),
        Node('f', 955, 295),
        Node('g', 955, 520),
        Node('h', 723, 520),
        Node('i', 723, 715),
        Node('j', 70, 488),
        Node('k', 70, 715),
        Node('l', 490, 715),
        Node('m', 955, 50),
        Node('n', 955, 715),
    ]

    graph = Graph(nodes, scale)

    graph.add_edge('a', 'k')
    graph.add_edge('j', 'k')
    graph.add_edge('j', 'b')
    graph.add_edge('j', 'c')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'd')
    graph.add_edge('d', 'e')
    graph.add_edge('e', 'f')
    graph.add_edge('f', 'g')
    graph.add_edge('g', 'h')
    graph.add_edge('h', 'i')
    graph.add_edge('l', 'h')
    graph.add_edge('l', 'i')
    graph.add_edge('l', 'a')
    graph.add_edge('m', 'd')
    graph.add_edge('n', 'i')

    graph.calculate_distances()

    return graph

