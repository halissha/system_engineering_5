VAR = int(input("Введите вариант: "))
COEFS = [[-1, -1], [1, -2], [-3, 2]]
BND_X = [0, VAR * 3]
BND_Y = [0, VAR * 4]
X_PTS = [-VAR * 1.5, VAR * 5]
RES = [-VAR * 2, VAR, VAR * 2]
if 1 <= VAR <= 5:
    INIT_APPROX = {"x1": VAR, "x2": VAR * 2}
elif 6 <= VAR <= 10:
    INIT_APPROX = {"x1": VAR * 4, "x2": VAR * 3}
elif 11 <= VAR <= 15:
    INIT_APPROX = {"x1": VAR * 2, "x2": VAR}
elif 16 <= VAR <= 20:
    INIT_APPROX = {"x1": VAR * 4, "x2": VAR * 2}
elif 21 <= VAR <= 25:
    INIT_APPROX = {"x1": VAR * 3, "x2": VAR * 2}
else:
    raise Exception("Указан неправильный номер варианта")