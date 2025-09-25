from node import Node
from infrastructure.edge import Edge

class Graph:
    def __init__(self):
        self.nodes = {} # id -> Node
        self.edges = [] # list of  Edge
        
    def add_node(self, id, x, y):
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
        n1.neighbots.append(n2)
        n2.neighbots.append(n1)