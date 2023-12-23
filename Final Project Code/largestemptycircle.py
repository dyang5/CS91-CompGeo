from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Point, Polygon

def find_largestempty_circle(coordinateLst):

    boundary_polygon = Polygon(coordinateLst)

    # determine largest indisk
    vor = Voronoi(coordinateLst)
    largest_min_distance = float('inf')
    optimal_vertex = None

    for voronoi_vertex in vor.vertices:
        min_distance = boundary_polygon.distance(Point(voronoi_vertex))
        if min_distance < largest_min_distance:
            largest_min_distance = min_distance
            optimal_vertex = voronoi_vertex

    largest_empty_circle_radii = boundary_polygon.distance(Point(optimal_vertex))
    return largest_empty_circle_radii