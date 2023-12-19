import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class PolygonDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.partitions = []
        self.polygon = None
        self.patches = []
        self.vertex_patches = []
        self.adding_vertices = True
        self.vertices = []
        self.current_polygon_x = []
        self.current_polygon_y = []
        self.current_polygon_vertices = []
        self.undo_stack = []

        self.ax.set_title("Circularity of Partitions Visualizer")
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)
        self.vertices.append([(0, 0), [0, 10], [10, 0], [10, 10]])
        self.ax.plot(0, 0, 'ro')
        self.ax.plot(0, 10, 'ro')
        self.ax.plot(10, 0, 'ro')
        self.ax.plot(10, 10, 'ro')

        self.fig.gca().set_aspect('equal')

        self.ax.set_axis_off()
        self.patches.append(mpl_patches.Rectangle((0, 0), 10, 10))
        self.ax.add_collection(PatchCollection(self.patches, facecolors='w', edgecolors='black'))

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_click(self, event):
        if self.adding_vertices and event.button == 1:  # Left mouse button
            print("GOOD " + str(event.xdata) + " " + str(event.ydata))
            self.add_point(event.xdata, event.ydata)

        elif not self.adding_vertices and event.button == 1:  # Left mouse button
            self.current_polygon_x = []
            self.current_polygon_y = []

            x_coord, y_coord = event.xdata, event.ydata
            is_contained = False

            for vertex in self.vertex_patches:
                # use transformed coordinates (coordinates are different once added to plot) -- debugging took 1 hour lol
                if vertex.contains_point(self.ax.transData.transform((x_coord, y_coord))):
                    is_contained = True
                    self.current_polygon_vertices.append(vertex.center)
                    break

            if not is_contained:
                print("Chosen point is not a valid vertex. Pick a valid vertex.")

        elif not self.adding_vertices and event.button == 3:  # Right mouse button
            self.create_polygon(self.current_polygon_vertices)
            self.current_polygon_vertices = []

    def on_key(self, event):
        if event.key == 'v':
            self.adding_vertices = not self.adding_vertices
            if self.adding_vertices:
                print("Adding vertices. Click to add a vertex.")
            else:
                print("Adding convex polygon partitions.")
        elif event.key == 'z':
            self.undo()

    def create_polygon(self, coordinate_lst):
        if coordinate_lst:
            polygon = Polygon(coordinate_lst, closed=True, facecolor='white', edgecolor='black')
            self.partitions.append(polygon)
            self.patches.append(polygon)
            self.ax.add_patch(polygon)
            self.fig.canvas.draw()
            self.save_state()

    def add_point(self, x, y):
        self.vertices.append((x, y))
        vertex = mpl_patches.Circle((x, y), radius=0.1, color='red')
        vertex.center = (x, y)
        self.vertex_patches.append(vertex)

        self.patches.append(vertex)
        self.ax.add_patch(vertex)
        self.fig.canvas.draw()
        self.save_state()

    def save_state(self):
        # Save the current state for undo
        self.undo_stack.append((self.vertices.copy(), self.partitions.copy()))

    def undo(self):
        if self.undo_stack:
            self.vertices, self.partitions = self.undo_stack.pop()
            self.ax.cla()
            self.ax.set_title("Circularity of Partitions Visualizer")
            self.ax.set_xlim(-1, 11)
            self.ax.set_ylim(-1, 11)

            for vertex in self.vertex_patches:
                self.ax.add_patch(vertex)

            for partition in self.partitions:
                self.ax.add_patch(partition)

            self.fig.canvas.draw()
            print("Undo complete.")
        else:
            print("Nothing to undo.")


if __name__ == "__main__":
    drawer = PolygonDrawer()

    plt.show()
