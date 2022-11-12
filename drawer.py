import math
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib import ticker
from maths import Maths

class Drawer:
    def __init__(self, variant):
        self.fig, self.ax = plt.subplots(figsize=(16, 7.5), dpi=100)
        self.var = variant

    def set_initial_settings(self):
        self.set_tick_params()
        self.set_axis_settings(self.var)
        self.draw_axis()

    def draw_bounds(self, fullpts):
        for pts in fullpts:
            plt.plot(pts["x"], pts["y"], color="k", linewidth=2)
        self.fill_bound(fullpts=fullpts)



    def fill_bound(self, fullpts):
        pts_pairs = Maths.make_pointpairs(fullpts)
        intersection_points = Maths.find_intersections(pts_pairs)
        intersection_points = sorted(intersection_points, key=self.clockwiseangle_and_distance)
        for i in range(len(intersection_points)):
            self.ax.scatter(intersection_points[i][0], intersection_points[i][1], zorder=3, color="k")
            self.ax.annotate(xy=[intersection_points[i][0], intersection_points[i][1]],
                             text=f"{chr(65 + i)}", xytext=(intersection_points[i][0] - 0.1,
                             intersection_points[i][1] + 1.5), size=12)
        self.draw_polygon(intersection_points)



    def set_tick_params(self, size=1, freq=4):
        self.ax.tick_params(which='minor', width=0.75, length=1, labelsize=size)
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(freq))
        self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(freq))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(freq))
        self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(freq))


    def set_axis_settings(self, var):
        self.ax.grid(which='major', color='k')
        xlim, ylim = (-12, var * 3.5), (-12, var * 3.5)
        self.ax.axis('equal')
        self.ax.set_ylim(xlim)
        self.ax.set_xlim(ylim)

    def draw_axis(self):
        offset = self.var * 3.5 - 1
        offset_x = offset * 1.6
        plt.plot([0, 0], [-16, offset], color="k", linewidth=4)
        plt.plot([-16, offset_x], [0, 0], color="k", linewidth=4)
        plt.plot([offset_x - 2, offset_x], [1, 0], color="k", linewidth=4)
        plt.plot([offset_x - 2, offset_x], [-1, 0], color="k", linewidth=4)
        plt.plot([-1, 0], [offset - 2, offset], color="k", linewidth=4)
        plt.plot([1, 0], [offset - 2, offset], color="k", linewidth=4)
        self.ax.annotate(xy=[0, offset], text="x2", xytext=(-4, offset - 2), size=12, weight='bold')
        self.ax.annotate(xy=[offset_x, 0], text="x1", xytext=(offset_x - 2, -3), size=12, weight='bold')


    def draw_polygon(self, points):
        p = Polygon(points, closed=True, facecolor='r', fill="r", alpha=0.4)
        self.ax.add_patch(p)

    def add_point_to_drawing(self, x1_, x1, x0, iter_, iters):
        x = [x1_[0], x1[0], x0[0]]
        y = [x1_[1], x1[1], x0[1]]
        self.ax.scatter(x, y, zorder=3, color="k", s=4)
        plt.plot(x, y, color="k", linewidth=0.5)
        if iter_ == 0 and iters < 3:
            self.ax.annotate(xy=[x[2], y[2]], text=f"X({iter_ + 1})", xytext=[x[2] + 1, y[2]], size=12)
            self.ax.annotate(xy=[x[1], y[1]], text=f"X({iter_})", xytext=[x[1] + 1, y[1]], size=12)
            self.ax.annotate(xy=[x[0], y[0]], text=f"X̄({iter_ + 1})", xytext=[x[0] + 1, y[0]], size=12)
        if iter_ == 1 and iters < 2:
            self.ax.annotate(xy=[x[2], y[2]], text=f"X({iter_ + 1})", xytext=[x[2] - 3.5, y[2] - 1], size=12)
            self.ax.annotate(xy=[x[0], y[0]], text=f"X̄({iter_ + 1})", xytext=[x[0] - 2, y[0] - 2.5], size=12)

    @staticmethod
    def show_drawing():
        plt.show()

    @staticmethod
    def clockwiseangle_and_distance(point, origin=(18.33, 3.76), refvec=(1, 0)):
        vector = [point[0] - origin[0], point[1] - origin[1]]
        lenvector = math.hypot(vector[0], vector[1])
        if lenvector == 0:
            return -math.pi, 0
        normalized = [vector[0] / lenvector, vector[1] / lenvector]
        dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]  # x1*x2 + y1*y2
        diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]  # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        if angle < 0:
            return 2 * math.pi + angle, lenvector
        return angle, lenvector
