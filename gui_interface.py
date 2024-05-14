import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import ast

from netmiko import ConnectHandler
from crawler import Crawler
from netgraph import InteractiveGraph


class GuiInterface:
    def __init__(self, net_devices):
        self.net_devices = net_devices
        self.root = tk.Tk()
        self.root.title("Net Topology Drawer")
        self.root.minsize(width=800, height=800)
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.draw_graph()
        self.root.mainloop()

    def draw_graph(self):
        g = nx.Graph()

        data = self.net_devices

        for router, connections in data.items():
            g.add_node(router)
            for connection in connections['connections'].values():
                g.add_edge(router, connection['identity'])

        edge_color = dict()
        for ii, edge in enumerate(g.edges):
            edge_color[edge] = 'tab:gray' if ii % 2 else 'tab:orange'

        node_color = dict()
        for i, node in enumerate(g.nodes):
            node_color[node] = 'tab:red' if i % 2 else 'tab:blue'

        fig, ax = plt.subplots(figsize=(8, 8))
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis([0, 1, 0, 1])
        ax.patch.set_edgecolor('black')
        ax.patch.set_linewidth(1)
        ax.autoscale_view(True, True, True)
        plot_instance = InteractiveGraph(
            g, node_size=5, node_color=node_color,
            node_labels=True, node_label_offset=0.1, node_label_fontdict=dict(size=20),
            edge_color=edge_color, edge_width=1, ax=ax, scale=(1, 1))

        interface_labels = []
        edges = []

        # [[R1, R2], , ],
        # [[R1, R2], , ],
        # [[R2, R3], , ],
        # ...

        for router, connections in data.items():
            for connection in connections['connections'].values():
                if [connection['identity'], router] in edges:
                    continue

                edges.append([router, connection['identity']])

                try:
                    interface_labels.append([[router, connection['identity']], 0.2, connection['interface']])
                    interface_labels.append([[router, connection['identity']], 0.8, connection['interface-name']])
                except KeyError:
                    print(f"Nie dodano interfejsu dla krawedzi {router}-{connection['identity']}")

        print(f"Zarejestrowane etykiety: {interface_labels}")

        def get_label_position(edge, edge_label_position, node_positions):
            v1, v2 = edge
            dxy = node_positions[v2] - node_positions[v1]
            xy = edge_label_position * dxy + node_positions[v1]
            angle = np.arctan2(dxy[1], dxy[0]) * 360 / (2.0 * np.pi)

            # reduce overlap with nodes
            if 90 <= (angle % 360) < 270:
                if edge_label_position < 0.5:
                    horizontal_alignment = "right"
                else:
                    horizontal_alignment = "left"
            else:
                if edge_label_position < 0.5:
                    horizontal_alignment = "left"
                else:
                    horizontal_alignment = "right"

            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < - 90:
                angle += 180

            return xy, angle, horizontal_alignment

        interface_label_text_objects = []
        for edge, edge_label_position, label in interface_labels:
            (x, y), angle, ha = get_label_position(edge, edge_label_position, plot_instance.node_positions)
            text_object = ax.text(x, y, label, rotation=angle, rotation_mode="anchor", va="center", ha=ha)
            interface_label_text_objects.append(text_object)

        def update_label_positions(event):
            for (edge, edge_label_position, _), text_object in zip(interface_labels, interface_label_text_objects):
                xy, angle, ha = get_label_position(
                    edge, edge_label_position, plot_instance.node_positions)
                text_object.set_position(xy)
                text_object.set_rotation(angle)
                text_object.set_horizontalalignment(ha)

        fig.canvas.mpl_connect('button_release_event', update_label_positions)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
