import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
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
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_click(self, event):
        # if in adding vertices stage and left mouse button is clicked
        if self.adding_vertices and event.button == 1:  
            print("GOOD " + str(event.xdata) + " " + str(event.ydata))
            self.add_point(event.xdata, event.ydata)
            
        # set up polygon creation
        elif not self.adding_vertices:
            self.current_polygon_x = []
            self.current_polygon_y = []

            if event.button == 1:
                xCoord = event.xdata
                yCoord = event.ydata
                isContained = False

                for vertex in self.vertex_patches:

                    # may need case where same vertex is clicked twice

                    # use transformed coordinates (coordinates are different once added to plot) --  debugging took 1 hour lol
                    if vertex.contains_point(self.ax.transData.transform((xCoord, yCoord))):
                        isContained = True
                        self.current_polygon_vertices.append(vertex.center)
                        break
                    
                if not isContained:
                    print("Chosen point is not a valid vertex. Pick a valid vertex.")        

            elif event.button == 3:
                print(self.current_polygon_vertices)
                if (len(self.current_polygon_vertices) < 3):
                    print("Need at least 3 vertices.")
                else:
                    self.create_polygon(self.current_polygon_vertices)
                    self.current_polygon_vertices = [ ]


        elif not self.adding_vertices and event.button == 3:  # Right mouse button
            self.finish_polygon()

    def on_key(self, event):
        # vertex addition phase
        if event.key == 'v':
            self.adding_vertices = not self.adding_vertices    
            if self.adding_vertices:
                print("Adding vertices. Click to add a vertex.")
            else:
                print("Adding convex polygon partitions.")

        # set up phase
        elif event.key == 't':
            self.setup()

    def setup(self):
        vertex_coordinates = [(0, 0), [0, 10], [10, 0], [10, 10]]
        self.vertices.append(vertex_coordinates)

        for coord in vertex_coordinates:
            x, y = coord
            vertex = mpl.patches.Circle((x, y), radius = 0.1, color = 'red')
            vertex.center = coord
            self.vertex_patches.append(vertex)

            self.patches.append(vertex)
            self.ax.add_patch(self.patches[len(self.patches) - 1])
            self.fig.canvas.draw()
        self.fig.gca().set_aspect('equal')

        self.ax.set_axis_off()
        self.patches.append(mpl.patches.Rectangle((0, 0),10,10))
        self.ax.add_collection(PatchCollection(self.patches, facecolors='w', edgecolors='black'))        
        self.fig.canvas.draw()
    
    def create_polygon(self, coordinateLst):
        self.partitions.append(Polygon(coordinateLst, closed=True, facecolor = 'white', edgecolor='black'))
        self.patches.append(self.partitions[len(self.partitions) - 1])
        self.ax.add_patch(self.partitions[len(self.partitions) - 1])
        self.fig.canvas.draw()
        self.save_state()
        

    def add_point(self, x, y):
        self.vertices.append((x, y))
        vertex = mpl.patches.Circle((x, y), radius = 0.1, color = 'red')
        vertex.center = (x, y)
        self.vertex_patches.append(vertex)

        self.patches.append(vertex)
        self.ax.add_patch(self.patches[len(self.patches) - 1]) # (zorder gives priority to patches)
        self.fig.canvas.draw()
        self.save_state()


    # def start_polygon(self, x, y):
    #     self.polygon = [((x, y))]
    #     self.patches = [Polygon(self.polygon, closed=False, edgecolor='r')]
    #     self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
    #     self.fig.canvas.draw()

    # def finish_polygon(self):
    #     if self.polygon is not None:
    #         self.polygon.append(self.polygon[0])
    #         self.patches[0] = Polygon(self.polygon, closed=True, edgecolor='r')
    #         self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
    #         self.fig.canvas.draw()
    #         self.polygon = None

    # keep track of states in stack
    def save_state(self):
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
