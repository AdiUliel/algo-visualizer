<img width="1187" height="692" alt="_דיאגרמה ללא שם_ drawio (1)" src="https://github.com/user-attachments/assets/8dcc9778-5147-452a-a6ec-e54b05b23b07" />

# Algorithm Visualizer
A tool for exploring algorithms visually.
Currently supports BFS and DFS.
This tool is implemented in Python (specifically, Pygame).

## Features
Step-by-step execution using generators (yield)
Smooth animations for node discovery and traversal
Visual indication of:
Visited / visiting / unvisited nodes
Active cursor on edges
Queue (BFS) or Stack (DFS)
Manual stepping or autoplay mode
Load custom graphs from JSON files
Simple UI for algorithm selection

## Project Structure
```text
algo-visualizer/
│
├── requirements.txt
├── README.md
└── src/
    ├── main.py              # Pygame entry point
    ├── app_controller.py    # Tkinter UI for algorithm selection
    │
    ├── infrastructure/      # Graph data structures
    │   ├── graph.py
    │   ├── node.py
    │   └── edge.py
    │
    ├── algorithms/          # Algorithm implementations
    │   ├── bfs.py
    │   ├── dfs.py
    │   └── animation_helpers.py
    │
    └── visualizer.py        # Rendering and drawing logic
```

## How to Run
1. Clone the repo
2. Install the requirements:
    pip install -r requirements.txt
3. Run it:
    * Either with the algorithm picker for making more manual selections:
        python -m src.app_controller
    * Or, directly launch the visualizer with a demo graph:
        python -m src.main

## Controls
    Key 	    Action
    B   	    Start BFS
    D	        Start DFS
    Space       Execute one step
    P	        Toggle autoplay
    R   	    Reset graph state
    ESC/Q	    Quit

## Custom Graph
You can load your own graph by filling the following JSON format.
* Each node must include screen coordinates (x,y) in order to be visualized.
```text
{
  "directed": false,
  "nodes": [
    { "id": 1, "x": 150, "y": 100 },
    { "id": 2, "x": 300, "y": 200 }
  ],
  "edges": [
    [1, 2],
    [2, 3]
  ]
}
```