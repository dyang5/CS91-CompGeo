import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull

def largest_inscribed_circle(vertices):
    convex_hull = ConvexHull(vertices)
    convex_hull_equations = convex_hull.equations

    norm_vector = np.reshape(np.linalg.norm(convex_hull_equations[:, :-1], axis=1),
        (convex_hull_equations.shape[0], 1))
    c = np.zeros((convex_hull_equations.shape[1],))
    c[-1] = -1
    A = np.hstack((convex_hull_equations[:, :-1], norm_vector))
    b = - convex_hull_equations[:, -1:]
    res = linprog(c, A_ub=A, b_ub=b, bounds=(None, None))
    x = res.x[:-1]
    y = res.x[-1]
    return x, y

# Example usage:
vertices = np.array([[0, 0], [1, 0], [1, 1], [0.5, 2], [0, 1]])

circle_center, circle_radius = largest_inscribed_circle(vertices)

print(f'Largest Inscribed Circle Center: {circle_center}')
print(f'Largest Inscribed Circle Radius: {circle_radius}')
