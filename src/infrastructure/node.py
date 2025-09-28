# node.py
class Node:
    def __init__(self, id, x, y):
        self.id = id # string or int - identifier
        self.state = "unvisited" # unvisited,visiting,visited
        self.parent = None
        self.neighbors = []  # adjacency list
        self.x = x
        self.y = y
        # x and y are parameters for visualization - where do we draw the node on the screen
        self.tint = None     # (rgb - optional)