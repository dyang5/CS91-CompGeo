import numpy as np
from scipy.optimize import minimize
from shapely.geometry import Point, Polygon
from scipy.spatial import ConvexHull

def find_chebyshev_center(vertices):
    def objective_function(center):
        polygon = Polygon(vertices)
        # Minimize the negative of the distance from center to polygon's exterior
        return polygon.distance(Point(center))

    # Initial guess for the Chebyshev center
    initial_guess = np.mean(vertices, axis=0)

    # Constraints: The center must be inside the convex polygon
    convex_hull = ConvexHull(vertices)
    convex_hull_equations = convex_hull.equations
    constraints = [{'type': 'ineq', 'fun': lambda center, eq=eq: np.dot(eq[:-1], center) + eq[-1]} for eq in convex_hull_equations]

    # Minimize the negative of the distance to find the Chebyshev center
    result = minimize(objective_function, initial_guess, constraints=constraints)

    return result.x