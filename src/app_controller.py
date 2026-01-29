import tkinter as tk
from tkinter import ttk

class PickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algo Visualizer Launcher")
        self.geometry("300x200")
        self.resizable(False, False)

        self.autoplay_var = tk.BooleanVar(value=False)

        frm = ttk.Frame(self, padding=20)
        frm.pack(expand=True, fill="both")

        ttk.Label(frm, text="Graph Editor Ready", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Checkbutton(frm, text="Start with Autoplay", variable=self.autoplay_var).pack(pady=10)
        
        ttk.Button(frm, text="Launch Visualizer", command=self.on_start).pack(pady=10)

    def on_start(self):
        autoplay = self.autoplay_var.get()
        self.destroy()
        
        from src.main import run_visualizer
        from src.infrastructure.graph import build_demo_graph
        
        run_visualizer(algorithm=None, start_id=1, auto_play_start=autoplay, graph=build_demo_graph())

if __name__ == "__main__":
    app = PickerApp()
    app.mainloop()