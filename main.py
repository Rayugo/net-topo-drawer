import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import ast
import numpy as np

from netgraph import InteractiveGraph


def draw_graph(canvas):
    with open('test_data.txt', 'r') as test_file:
        content = test_file.read()
        data = ast.literal_eval(content)

    # Tworzenie grafu
    G = nx.Graph()

    # Dodawanie węzłów i krawędzi do grafu
    for router, connections in data.items():
        G.add_node(router)
        for connection in connections['connections'].values():
            G.add_edge(router, connection['identity'])

    # Rysowanie grafu
    pos = nx.spring_layout(G)  # układ wiosenny
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=10, font_weight='bold', width=2)


def main():
    root = tk.Tk()
    root.title("Net-Topology Drawer")

    # Kontener dla wykresu
    frame = tk.Frame(root)
    frame.pack()

    # Tworzenie wykresu
    fig = plt.figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    draw_graph(canvas)

    root.mainloop()


if __name__ == "__main__":
    main()
