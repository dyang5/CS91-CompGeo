import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from matplotlib.widgets import PolygonSelector
fig2, ax2 = plt.subplots()
fig2.show()
plt.get_current_fig_manager().show()


selector2 = PolygonSelector(ax2, lambda *args: None)

print("Click on the figure to create a polygon.")
print("Press the 'esc' key to start a new polygon.")
print("Try holding the 'shift' key to move all of the vertices.")
print("Try holding the 'ctrl' key to move a single vertex.")

if __name__ == "__main__":
    plt.show()
