import math
import numpy as np
from shapely.geometry import LineString
from scipy.optimize import linprog
import sympy as sym
from const import VAR, COEFS, BND_X, BND_Y, X_PTS, RES, INIT_APPROX

class Maths:

    @staticmethod
    def make_pointpairs(fullpts):
        pts_pairs = []
        for pts in fullpts:
            for pt in fullpts:
                pts_pairs.append({"y1": pts["y"], "y2": pt["y"], "x1": pts["x"], "x2": pt["x"]})
        return pts_pairs

    @staticmethod
    def find_intersections(pts_pairs):
        intersection_points = []
        for point in pts_pairs:
            first_line = LineString(np.column_stack((point["x1"], point["y1"])))
            second_line = LineString(np.column_stack((point["x2"], point["y2"])))
            intersection = first_line.intersection(second_line)
            if intersection.geom_type == 'Point':
                intersection_points.append([*intersection.coords.xy[0].tolist(), *intersection.coords.xy[1].tolist()])
        for point in intersection_points:
            if point[0] < 0:
                intersection_points.remove(point)
        intersection_points = [list(x) for x in set(tuple(x) for x in intersection_points)]
        return intersection_points

    @staticmethod
    def maximize(name: str, res: list, bnd_x: list, bnd_y: list, grad: list, coefs: list):
        lin_res = linprog(c=grad, A_ub=coefs, b_ub=res,
                          bounds=[bnd_x, bnd_y], method="highs")
        result = {"name": name, "optimal_val": lin_res}
        return result

    @staticmethod
    def find_func_points(C, x_pts, x_coef, dep=True):
        points = {"x": [], "y": []}
        for val in x_pts:
            if not dep:
                points["x"].append(C + (x_coef * val))
                points["y"].append(val)
            else:
                points["y"].append(C + (x_coef * val))
                points["x"].append(val)
        return points

    @staticmethod
    def find_p_x0(coefs, point):
        result = (point[0] + point[1] - coefs[0]) ** 2 + \
                 (-3 * point[0] + point[1] - coefs[1]) ** 2 + \
                 (point[0] - 3 * point[1] - coefs[2]) ** 2
        return result

    @staticmethod
    def define_grad_x1(fvec, x1_, x2_):
        C1, C2, C3 = fvec[0], fvec[1], fvec[2]
        x1 = sym.Symbol('x1')
        x2 = sym.Symbol('x2')
        expr = sym.expand((x1 + x2 - C1) ** 2) + \
               sym.expand((-3 * x1 + x2 - C2) ** 2) + \
               sym.expand((x1 - 3 * x2 - C3) ** 2)
        deriv = sym.diff(expr, x1)
        grad = deriv.subs(x1, x1_)
        grad_ = grad.subs(x2, x2_)
        return grad_

    @staticmethod
    def define_grad_x2(fvec, x1_, x2_):
        C1, C2, C3 = fvec[0], fvec[1], fvec[2]
        x1 = sym.Symbol('x1')
        x2 = sym.Symbol('x2')
        expr = sym.expand((x1 + x2 - C1) ** 2) + \
               sym.expand((-3 * x1 + x2 - C2) ** 2) + \
               sym.expand((x1 - 3 * x2 - C3) ** 2)
        deriv = sym.diff(expr, x2)
        grad = deriv.subs(x2, x2_)
        grad_ = grad.subs(x1, x1_)
        return grad_

    @staticmethod
    def make_F_vector(values: list):
        return [res["optimal_val"].fun * -1 for res in values]

    @staticmethod
    def set_x1_matrix(point, x1, x2):
        x = sym.Symbol('λ')
        return [x1 + round(point[0] - x1, 5) * x, x2 + round(point[1] - x2, 5) * x]

    @staticmethod
    def find_lambda(matrix, F):
        x = sym.Symbol('λ')
        syms = sym.expand((matrix[0] + matrix[1] - F[0]) ** 2) + \
               sym.expand((-3 * (matrix[0]) + matrix[1] - F[1]) ** 2) + \
               sym.expand((matrix[0] + -3 * matrix[1] - F[2]) ** 2)
        deriv = sym.diff(syms, x)
        coef_dict = deriv.as_coefficients_dict(x)
        lambda_ = -coef_dict[1] / coef_dict[x]
        return lambda_

    @staticmethod
    def conduct_initial_maximizations():
        res = [Maths.maximize(name="x1 + x2 -> max", coefs=COEFS, res=RES, bnd_x=BND_X, bnd_y=BND_Y, grad=[-1, -1]),
               Maths.maximize(name="-3x1 + x2 -> max", coefs=COEFS, res=RES, bnd_x=BND_X, bnd_y=BND_Y, grad=[3, -1]),
               Maths.maximize(name="x1 - 3x2 -> max", coefs=COEFS, res=RES, bnd_x=BND_X, bnd_y=BND_Y, grad=[-1, 3])]
        return res


    @staticmethod
    def conduct_maximization(grad):
        res = [Maths.maximize(name=f"{grad}x1 + {grad}x2 -> max", coefs=COEFS, res=RES, bnd_x=BND_X,
                              bnd_y=BND_Y, grad=grad)]
        return res

    @staticmethod
    def find_all_func_points():
        fullpts = [Maths.find_func_points(C=VAR * 2, x_pts=X_PTS, x_coef=-1),
                   Maths.find_func_points(C=-VAR / 2, x_pts=X_PTS, x_coef=0.5),
                   Maths.find_func_points(C=VAR, x_pts=X_PTS, x_coef=1.5),
                   Maths.find_func_points(C=BND_X[1], x_pts=X_PTS, x_coef=0),
                   Maths.find_func_points(C=BND_Y[1], x_pts=X_PTS, x_coef=0, dep=False)]
        return fullpts

    @staticmethod
    def find_x1_x2():
        return INIT_APPROX["x1"], INIT_APPROX["x2"]






