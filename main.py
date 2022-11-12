from drawer import Drawer
from maths import Maths
import sympy as sym
from printer import Printer
from const import VAR

drawer = Drawer(VAR)

def manage_drawer(pts):
    drawer.set_initial_settings()
    drawer.draw_bounds(pts)
    drawer.show_drawing()

def manage_maximization_of_f_functions():
    optimal_vals = Maths.conduct_initial_maximizations()
    Printer.print_maximizations(result=optimal_vals, func_name="Функция")
    return optimal_vals

def manage_optimal_vector(values: list):
    F_vec = Maths.make_F_vector(values=values)
    Printer.print_F_vector(F_vec)
    return F_vec

def manage_newfunc_maximization(grad):
    res = Maths.conduct_maximization(grad=grad)
    Printer.print_maximizations(res, func_name="Составим вспомогательную функцию")
    return res[0]["optimal_val"].x

def manage_x1_matrix(point_x1, x1, x2):
    matr = Maths.set_x1_matrix(point_x1, x1, x2)
    Printer.print_x1_matrix(matr)
    return matr

def conduct_iterations(F):
    x = sym.Symbol('λ')
    x1, x2 = Maths.find_x1_x2()
    iterations = int(input("\nУкажите число итераций: "))
    for iteration in range(iterations):
        Printer.print_iteration_number(iteration)
        grad_x1 = Maths.define_grad_x1(F, x1_=x1, x2_=x2)
        grad_x2 = Maths.define_grad_x2(F, x1_=x1, x2_=x2)
        point_x1 = manage_newfunc_maximization(grad=[grad_x1, grad_x2])
        p_x0 = Maths.find_p_x0(coefs=F, point=[x1, x2])
        Printer.print_p_x(number=0, res=p_x0)
        matrix = manage_x1_matrix(point_x1, x1=x1, x2=x2)
        lambda_ = Maths.find_lambda(matrix=matrix, F=F)
        Printer.print_lambda(lambda_)
        drawer.add_point_to_drawing(point_x1, [x1, x2], [matrix[0].subs(x, lambda_),  matrix[1].subs(x, lambda_)],
                                    iteration, iterations)
        x1, x2 = matrix[0].subs(x, lambda_), matrix[1].subs(x, lambda_)
        Printer.print_new_point(x1, x2)
        p_x1 = Maths.find_p_x0(coefs=F, point=[x1, x2])
        Printer.print_p_x(number=1, res=p_x1)
        if p_x0 - p_x1 < 0.1:
            print(f"max iter: {iteration}")
            break


if __name__ == '__main__':
    optimal_values = manage_maximization_of_f_functions()
    F_vector = manage_optimal_vector(values=optimal_values)
    conduct_iterations(F=F_vector)
    full_pts = Maths.find_all_func_points()
    manage_drawer(full_pts)


