import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import smallestcircumscribingcircle
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from scipy.spatial import Voronoi, voronoi_plot_2d

class PolygonDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        # set up
        self.partitions = []
        self.patches = []
        self.vertex_patches = []
        self.adding_vertices = True
        # self.vertices = []
        self.current_polygon_x = []
        self.current_polygon_y = []
        self.current_polygon_vertices = []
        self.undo_stack = []

        # plot visualizer
        self.ax.set_axis_off()
        self.ax.set_title("Circularity of Partitions Visualizer")
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)

        # user input
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

                    # use transformed coordinates (coordinates are different once added to plot)
                    if vertex.contains_point(self.ax.transData.transform((xCoord, yCoord))):
                        isContained = True
                        self.current_polygon_vertices.append(vertex.center)
                        break
                    
                if not isContained:
                    print("Chosen point is not a valid vertex. Pick a valid vertex.")

            elif event.button == 3:
                print(self.current_polygon_vertices)
                if (len(self.current_polygon_vertices) < 3):
                    print("Need at least 3 vertices. Repick at least 3 vertices for polygon.")
                else:
                    self.create_polygon(self.current_polygon_vertices)
                # reset polygon vertices
                self.current_polygon_vertices = []


        elif not self.adding_vertices and event.button == 3:
            self.finish_polygon()

    def on_key(self, event):
        # vertex addition phase
        if event.key == 'v':
            self.adding_vertices = not self.adding_vertices    
            if self.adding_vertices:
                print("Adding vertices. Click to add a vertex.")
            else:
                print("Adding convex polygon partitions.")

        # undo button
        elif event.key == 'z':
            self.undo()

        # set up visualization
        elif event.key == 't':
            self.setup()

        # when done adding polygons
        elif event.key == 'd':
            self.calculate_circularity()

    def setup(self):  
        vertex_coordinates = [(0, 0), [0, 10], [10, 0], [10, 10]]
        # self.vertices.append(vertex_coordinates)

        for coord in vertex_coordinates:
            x, y = coord
            vertex = mpl.patches.Circle((x, y), radius = 0.1, color = 'red', zorder = 1000) # zorder gives priority to vertices, so they don't get blocked by polygons
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

        centroid = np.average(coordinateLst, axis=0)
        self.add_label(centroid[0], centroid[1], len(self.partitions))
        

    def add_point(self, x, y):
        # self.vertices.append((x, y))
        vertex = mpl.patches.Circle((x, y), radius = 0.1, color = 'red', zorder = 1000) 
        vertex.center = (x, y)
        self.vertex_patches.append(vertex)

        self.patches.append(vertex)
        self.ax.add_patch(self.patches[len(self.patches) - 1]) 
        self.fig.canvas.draw()
        self.save_state()

    # keep track of states in "stack"
    def save_state(self):
        self.undo_stack.append((self.vertex_patches.copy(), self.partitions.copy()))

    # undo last action
    def undo(self):
        if len(self.undo_stack) >= 2:
            self.undo_stack.pop()
            self.vertex_patches, self.partitions = self.undo_stack.pop()

            self.setup()
            for vertex in self.vertex_patches:
                self.ax.add_patch(vertex)

            for partition in self.partitions:
                self.ax.add_patch(partition)

            self.fig.canvas.draw()
            print("Undo complete.")
        else:
            print("Nothing to undo.")

    def add_label(self, x, y, label):
        self.ax.text(x, y, label, fontsize=5, color='black', ha='center', va='center')
        self.fig.canvas.draw()
        # self.save_state()         

    def calculate_circularity(self):
        print("Finding polygonal piece with maximum circularity.")

        # think about how to calculate circiumradius and inradius
        # https://math.stackexchange.com/questions/1948356/largest-incircle-inside-a-quadrilateral-radius-calculation (radius of largest indisk)
        # (finding smallest circumscribing circle
        # is this an instance of smallest circle problem?
        # https://www.nayuki.io/res/smallest-enclosing-circle/smallestenclosingcircle.py
        # https://math.stackexchange.com/questions/1835931/largest-enclosed-inscribed-circle-in-cloud-of-points (find Voronoi vertex that maximizes the distance to closest site)

        min_circularity = float('inf')
        min_circularity_index = 0
        circularities = []
        circumcircles = []
        indisks = []

        for poly in self.partitions:
            coordinateLst = poly.get_xy()

            # determine smallest circumscribing circle
            circum = smallestcircumscribingcircle.make_circle(coordinateLst)
            circumcircles.append(circum)
            circumcircle_radii = circum[2]

            # determine largest indisk
            vor = Voronoi(coordinateLst)
            largest_min_distance = float('inf')
            optimal_vertex = None

            for voronoi_vertex in vor.vertices:
                min_distance = float('inf')
                for coordinate in coordinateLst:
                    min_distance = min(np.linalg.norm(coordinate - voronoi_vertex), min_distance)
                if min_distance < largest_min_distance:
                    largest_min_distance = min_distance
                    optimal_vertex = voronoi_vertex
                indisks.append((optimal_vertex[0], optimal_vertex[1], largest_min_distance))

            indisk_radii = largest_min_distance

            circularity = circumcircle_radii / indisk_radii
            circularities.append(circularity)
            if circularity < min_circularity:
                min_circularity = circularity
                min_circularity_index = len(circularities) - 1

        print(circularities)
        print(min_circularity)

if __name__ == "__main__":
    drawer = PolygonDrawer()
    
    plt.show()
