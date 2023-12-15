import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class PolygonDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.polygon = None
        self.patches = []

        self.ax.set_title("Circularity of Partitions Visualizer")
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.fig.gca().set_aspect('equal')

        self.ax.set_axis_off()
        self.patches.append(mpl.patches.Rectangle((-5,-5),10,10))
        self.ax.add_collection(PatchCollection(self.patches, facecolors='w', edgecolors='black'))

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.button == 1:  # Left mouse button
            print("GOOD " + str(event.xdata) + " " + str(event.ydata))

            if self.polygon is None:
                self.start_polygon(event.xdata, event.ydata)
            else:
                self.add_point(event.xdata, event.ydata)
        elif event.button == 3:  # Right mouse button
            self.finish_polygon()

    def start_polygon(self, x, y):
        self.polygon = [((x, y))]
        self.patches = [Polygon(self.polygon, closed=False, edgecolor='r')]
        self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
        self.fig.canvas.draw()

    def add_point(self, x, y):
        self.polygon.append((x, y))
        self.patches[0] = Polygon(self.polygon, closed=False, edgecolor='r')
        self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
        self.fig.canvas.draw()

    def finish_polygon(self):
        if self.polygon is not None:
            self.polygon.append(self.polygon[0])  # Close the polygon
            self.patches[0] = Polygon(self.polygon, closed=True, edgecolor='r')
            self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
            self.fig.canvas.draw()
            self.polygon = None


if __name__ == "__main__":
    drawer = PolygonDrawer()
    plt.show()
