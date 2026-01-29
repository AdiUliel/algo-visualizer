from .node import Node
from .edge import Edge

class Graph:
    def __init__(self, directed=False):
        self.nodes = {}         
        self.edges = []         
        self.directed = directed
        self.fx = {}
        self.speed_factor = 0.5
        
    def add_node(self, id, x, y):
        if id in self.nodes:
            raise ValueError(f"Node with id {id} already exists")
        node = Node(id, x, y)
        self.nodes[id] = node
        return node
    
    def add_edge(self, id1, id2, weight=1):
        if id1 not in self.nodes or id2 not in self.nodes:
            raise ValueError("Both nodes must exit in the graph")
        n1, n2 = self.nodes[id1], self.nodes[id2]
        
        edge = Edge(n1, n2, weight)
        self.edges.append(edge)
        
        n1.neighbors.append(n2)
        if not self.directed:
            n2.neighbors.append(n1)

    def get_edge_weight(self, id1, id2):
        for edge in self.edges:
            if edge.start.id == id1 and edge.end.id == id2:
                return edge.weight
            if not self.directed and edge.start.id == id2 and edge.end.id == id1:
                return edge.weight
        return 1
            
    def reset_states(self):
        for node in self.nodes.values():
            node.state = "unvisited"
            node.parent = None
            node.tint = None
        self.fx.clear()

def build_demo_graph() -> Graph:
    g = Graph(directed=False)
    g.add_node(1, 150, 200)
    g.add_node(2, 350, 100)
    g.add_node(3, 550, 200)
    g.add_node(4, 250, 450)
    g.add_node(5, 450, 450)

    g.add_edge(1, 2, 2)
    g.add_edge(2, 3, 3)
    g.add_edge(1, 4, 6)
    g.add_edge(2, 4, 2)
    g.add_edge(4, 5, 1)
    g.add_edge(3, 5, 5)
    return g