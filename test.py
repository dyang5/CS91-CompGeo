import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class PolygonDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.vertices = []
        self.polygon = None
        self.patches = []
        self.is_drawing_points = True

        self.ax.set_title("Interactive Polygon Drawer")
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)
        self.vertices.append([(0, 0), [0, 10], [10, 0], [10, 10]])
        self.ax.plot(0, 0, 'ro')
        self.ax.plot(0, 10, 'ro')
        self.ax.plot(10, 0, 'ro')
        self.ax.plot(10, 10, 'ro')
        self.patches.append(mpl.patches.Rectangle((0, 0),10,10))
        self.ax.add_collection(PatchCollection(self.patches, facecolors='w', edgecolors='black'))
        self.fig.canvas.draw()

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_click(self, event):
        if self.is_drawing_points and event.button == 1:  # Left mouse button
            self.add_vertex(event.xdata, event.ydata)
        elif not self.is_drawing_points and event.button == 1:  # Left mouse button
            self.create_polygon()

    def on_key(self, event):
        if event.key == 't':
            self.is_drawing_points = not self.is_drawing_points
            if self.is_drawing_points:
                print("Drawing points mode. Click to add vertices.")
            else:
                print("Polygon creation mode. Click to create a polygon.")

    def add_vertex(self, x, y):
        self.vertices.append((x, y))
        self.ax.plot(x, y, 'ro')  # Mark the vertex with a red dot
        self.fig.canvas.draw()

    def create_polygon(self):
        if len(self.vertices) >= 3:
            self.vertices.append(self.vertices[0])  # Close the polygon
            self.polygon = Polygon(self.vertices, closed=True, edgecolor='r')
            self.patches = [self.polygon]
            self.ax.patches = []
            self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
            self.fig.canvas.draw()
            self.vertices = []
            print("Polygon created.")
        else:
            print("At least 3 vertices are required to create a polygon.")

if __name__ == "__main__":
    drawer = PolygonDrawer()
    print("Drawing points mode. Click to add vertices.")
    plt.show()
