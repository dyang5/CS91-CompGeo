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
        self.vertex_patches = []
        self.adding_vertices = True
        self.vertices = []

        self.ax.set_title("Circularity of Partitions Visualizer")
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)
        self.ax.plot(0, 0, 'ro')
        self.ax.plot(0, 10, 'ro')
        self.ax.plot(10, 0, 'ro')
        self.ax.plot(10, 10, 'ro')

        self.fig.gca().set_aspect('equal')

        self.ax.set_axis_off()
        self.patches.append(mpl.patches.Rectangle((0, 0),10,10))
        self.ax.add_collection(PatchCollection(self.patches, facecolors='w', edgecolors='black'))

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
                    # use transformed coordinates (coordinates are different once added to plot) --  debugging took 1 hour lol
                    if vertex.contains_point(self.ax.transData.transform((xCoord, yCoord))):
                        isContained = True
                        self.current_polygon_x.append(event.xdata)
                        self.current_polygon_y.append(event.ydata)
                        break
                    
                if not isContained:
                    print("NOT CONTAINED")        

            elif event.button == 3:
                self.create_polygon(self.current_polygon_x, self.current_polygon_y)


        elif not self.adding_vertices and event.button == 3:  # Right mouse button
            self.finish_polygon()

    def on_key(self, event):
        if event.key == 'v':
            self.adding_vertices = not self.adding_vertices    
            if self.adding_vertices:
                print("Adding vertices. Click to add a vertex.")
            else:
                print("Adding convex polygon partitions.")
    
    def create_polygon(self, xLst, yLst):
        print("HELLO")

    def start_polygon(self, x, y):
        self.polygon = [((x, y))]
        self.patches = [Polygon(self.polygon, closed=False, edgecolor='r')]
        self.ax.add_collection(PatchCollection(self.patches, facecolors='b', edgecolors='r'))
        self.fig.canvas.draw()

    def add_point(self, x, y):
        self.vertices.append((x, y))
        vertex = mpl.patches.Circle((x, y), radius = 1, color = 'red')
        vertex.center = (x, y)
        self.vertex_patches.append(vertex)

        self.patches.append(vertex)
        self.ax.add_patch(self.patches[len(self.patches) - 1])
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
