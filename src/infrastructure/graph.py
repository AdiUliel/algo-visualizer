from .node import Node
from .edge import Edge

class Graph:
    def __init__(self, directed = False):
        self.nodes = {}         # id -> Node
        self.edges = []         # list of  Edge
        self.directed = directed
        self.fx = {}
        self.speed_factor = 0.5
        
    def add_node(self, id, x, y):
        if id in self.nodes:
            raise ValueError(f"Node with id {id} already exists")
        node = Node(id, x, y)
        self.nodes[id] = node
        return node
    
    def add_edge(self, id1, id2):
        if id1 not in self.nodes or id2 not in self.nodes:
            raise ValueError("Both nodes must exit in the graph")
        n1, n2 = self.nodes[id1], self.nodes[id2]
        
        # creating edge object
        edge = Edge(n1, n2)
        self.edges.append(edge)
        
        # updating adjacency
        n1.neighbors.append(n2)
        if not self.directed:
            n2.neighbors.append(n1)
            
    def reset_states(self):
        """
        Reset all nodes to unvisited before BFS/DFS
        """
        for node in self.nodes.values():
            node.state = "unvisited"
            node.parent = None
            node.tint = None
        self.fx.clear()