import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.infrastructure.graph import Graph, build_demo_graph
from src.main import run_visualizer

def load_graph_from_json(path: str) -> Graph:
    """
    טעינת גרף מקובץ JSON.
    פורמט מצופה לקשתות: [מקור, יעד, משקל] או [מקור, יעד]
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    directed = bool(data.get("directed", False))
    g = Graph(directed=directed)

    for n in data.get("nodes", []):
        g.add_node(int(n["id"]), int(n["x"]), int(n["y"]))

    for edge_data in data.get("edges", []):
        u = int(edge_data[0])
        v = int(edge_data[1])
        w = int(edge_data[2]) if len(edge_data) > 2 else 1
        g.add_edge(u, v, w)

    return g

class PickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algorithm Visualizer — Picker")
        self.resizable(False, False)
        self.geometry("+200+150")

        self.selected_algo = tk.StringVar(value="bfs")
        self.start_id_str  = tk.StringVar(value="1")
        self.autoplay_var  = tk.BooleanVar(value=False)
        self.graph_path    = tk.StringVar(value="")

        pad = {"padx": 10, "pady": 6}
        frm = ttk.Frame(self)
        frm.grid(row=0, column=0, sticky="nsew", **pad)

        ttk.Label(frm, text="Algorithm:").grid(row=0, column=0, sticky="w")
        algo_box = ttk.Frame(frm)
        algo_box.grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(algo_box, text="BFS", variable=self.selected_algo, value="bfs").pack(side="left")
        ttk.Radiobutton(algo_box, text="DFS", variable=self.selected_algo, value="dfs").pack(side="left")
        ttk.Radiobutton(algo_box, text="Dijkstra", variable=self.selected_algo, value="dijkstra").pack(side="left")

        ttk.Label(frm, text="Start node ID:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.start_id_str, width=12).grid(row=1, column=1, sticky="w")

        ttk.Checkbutton(frm, text="Autoplay", variable=self.autoplay_var).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Graph file (JSON):").grid(row=3, column=0, sticky="w")
        file_row = ttk.Frame(frm)
        file_row.grid(row=3, column=1, sticky="we")
        self.file_entry = ttk.Entry(file_row, textvariable=self.graph_path, width=26)
        self.file_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(file_row, text="Load…", command=self.pick_file).pack(side="left", padx=4)

        btn_row = ttk.Frame(frm)
        btn_row.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_row, text="Start", command=self.on_start).pack(side="left", padx=4)
        ttk.Button(btn_row, text="Cancel", command=self.destroy).pack(side="left", padx=4)

    def pick_file(self):
        path = filedialog.askopenfilename(
            title="Choose graph JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.graph_path.set(path)

    def on_start(self):
        try:
            start_id = int(self.start_id_str.get().strip())
        except ValueError:
            messagebox.showerror("Invalid input", "Start node ID must be an integer.")
            return

        algo = self.selected_algo.get().strip().lower()
        autoplay = bool(self.autoplay_var.get())

        try:
            if self.graph_path.get():
                g = load_graph_from_json(self.graph_path.get())
            else:
                g = build_demo_graph()
            
            if start_id not in g.nodes:
                messagebox.showerror("Invalid start node", f"Node {start_id} does not exist.")
                return
        except Exception as e:
            messagebox.showerror("Failed to load graph", str(e))
            return

        self.destroy()
        run_visualizer(algorithm=algo, start_id=start_id, auto_play_start=autoplay, graph=g)

if __name__ == "__main__":
    app = PickerApp()
    app.mainloop()