<img width="1187" height="692" alt="_דיאגרמה ללא שם_ drawio (1)" src="https://github.com/user-attachments/assets/8dcc9778-5147-452a-a6ec-e54b05b23b07" />

# Algorithm Visualizer
An interactive tool for exploring algorithms visually.
The visualizer allows you to easily build, edit, and traverse graphs - currently supports BFS,DFS amd Dijkstra algorithms.
This tool is implemented in Python (and Pygame).

## Features
* Real-time Interaction:
* Add/Delete Nodes: Build your graph from scratch on a blank canvas.
* Dynamic Edging: Connect nodes and assign weights with simple mouse controls.
* Traversal Animations.
* In-depth Algorithm Tracking:
    * Sidebar Data: Real-time view of the Queue, Stack, or Priority Queue.
    * Visit Log: A historical log of the traversal sequence.

## Project Structure
```text
algo-visualizer/
│
├── requirements.txt
├── README.md
└── src/
    ├── main.py
    ├── app_controller.py
    |   # this file is not being used in the current version.
    │
    ├── infrastructure/      # Graph data structures
    │   ├── graph.py
    │   ├── node.py
    │   └── edge.py
    │
    ├── algorithms/          # Algorithm implementations
    │   ├── bfs.py
    │   ├── dfs.py
    │   ├── dijkstra.py
    │   └── animation_helpers.py
    │
    └── visualizer.py        # Rendering, drawing and sidebar logic
```

## How to Run
1. Clone the repo
```text
git clone https://github.com/<your-username>/algo-visualizer.git
cd algo-visualizer
```
2. Install the requirements:
```text
pip install -r requirements.txt
```
3. Run it:
```text
python -m src.main
```


## Controls

### Graph Editing
| Key/Mouse | Action |
| :--- | :--- |
| **Left-Click** | Add a new Node |
| **Right-Click** | Connect two nodes (select first, then second) |
| **Double Right-Click** | Edit Edge weight (on the edge itself) |
| **DEL / Backspace** | Delete the hovered node or edge |
| **C** | **Clear Board**: Wipe all nodes and edges (requires confirmation) |

### Algorithm Execution
| Key | Action |
| :--- | :--- |
| **B** | Start **BFS** (Breadth-First Search) |
| **D** | Start **DFS** (Depth-First Search) |
| **K** | Start **Dijkstra's** Algorithm |
| **Space** | Execute one step |
| **P** | Toggle Autoplay |
| **O** | **Stop**: Reset states and return to Editor Mode |
| **ESC / Q** | Quit Application |