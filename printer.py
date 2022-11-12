class Printer:

    @staticmethod
    def print_x1_matrix(matr):
        print(f"X(1) матрица: {matr}")

    @staticmethod
    def print_F_vector(f):
        print(f"\nF-vector: {f}")

    @staticmethod
    def print_maximizations(result, func_name):
        print('\nCONDUCTED MAXIMIZATIONS:')
        for i in range(len(result)):
            print(f'\n----------------------------------------\n{func_name}: {result[i]["name"]}\n'
                  f'Оптимальное значение: {round(result[i]["optimal_val"].fun * -1, ndigits=2)}',
                  '\nВ точке:', list(result[i]["optimal_val"].x), '\n----------------------------------------')

    @staticmethod
    def print_iteration_number(idx):
        print(f"\n-------------ITERATION NUMBER {idx + 1}-------------")

    @staticmethod
    def print_lambda(lambda_):
        print(f"Lambda: {lambda_}")

    @staticmethod
    def print_new_point(x1, x2):
        print(f"Point X1: [{x1}, {x2}]")

    @staticmethod
    def print_p_x(number, res):
        print(f"p(X({number})): {res}")