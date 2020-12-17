import math
from random import randint
import matplotlib.pyplot as plt
import trojkat
# from shapely.geometry import Point, Polygon


class kolo:
    def __init__(self, x1, y1, promien):
        self.x1 = x1
        self.y1 = y1
        self.promien = promien

    def czywkole(self, xp, yp):
        result = False
        if math.hypot(xp-self.x1, yp-self.y1) <= self.promien:
            result = True
        if result:
            return f'Punkt ({xp},{yp}) należy do koła.'
        return f'Punkt ({xp},{yp}) nie należy do koła.'

    def __str__(self):
        return f'środek: ({self.x1},{self.y1}), promień: {self.promien}'


class elipsa:
    def __init__(self, x1, y1, mpolos, wpolos):
        self.x1 = x1
        self.y1 = y1
        self.mpolos = mpolos
        self.wpolos = wpolos

    def czywelipsie(self, xp, yp):
        result = False
        if ((xp-self.x1)^2)/(self.wpolos^2) + ((yp-self.y1)^2)/(self.mpolos^2) <= 1:
            result = True
        if result:
            return f'Punkt ({xp},{yp}) należy do elipsy.'
        return f'Punkt ({xp},{yp}) nie należy do elipsy.'

    def __str__(self):
        return f'środek: ({self.x1},{self.y1}), półoś wielka: {self.wpolos}, półoś mała: {self.mpolos}'

# ------------------------------------------------------------------------- #


class Points:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def calc_distance(p1, p2):
        return round(math.sqrt((p1.y - p2.y)**2 + (p1.x - p2.x)**2), 2)

    @staticmethod
    def display_points():
        # TODO create config file for plt styles
        plt.scatter([points[x].x for x in range(len(points))],
                    [points[y].y for y in range(len(points))], s=5, c='black')

    @staticmethod
    def get_rectangles():
        r = []
        for p1 in points:
            for p2 in points[points.index(p1) + 1::]:
                c = Points.calc_distance(p1, p2)
                for p3 in points[points.index(p1) + 1:points.index(p2):]:
                    a = Points.calc_distance(p1, p3)
                    b = Points.calc_distance(p2, p3)
                    if a != b:
                        if a**2 + b**2 == c**2:
                            if p3.y > p2.y:
                                p4 = [0, p1.y - p3.y + p2.y]
                            else:
                                p4 = [0, p1.y + abs(p3.y - p2.y)]
                            if p3.x > p1.x:
                                p4[0] = p1.x - p3.x + p2.x
                            else:
                                p4[0] = p1.x + abs(p3.x - p2.x)
                            p4 = tuple(p4)
                            p4 = Points(p4[0], p4[1])
                            if p4 in points:
                                r.append(Rect(p1, p2, p3, p4))
        return r


class Rect:

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.a = Points.calc_distance(p1, p2)
        self.b = Points.calc_distance(p2, p3)

    def __hash__(self):
        return hash((self.p1, self.p2, self.p3, self.p4))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.p1, self.p3, self.p2, self.p4 in [other.p1, other.p3, other.p2, other.p4]

    def display_rect(self, c):
        tmp_x = [getattr(p, 'x') for p in [self.p1, self.p3, self.p2, self.p4]]
        tmp_y = [getattr(p, 'y') for p in [self.p1, self.p3, self.p2, self.p4]]
        plt.scatter(tmp_x, tmp_y, s=7, c=c)
        tmp_x.append(tmp_x[0])
        tmp_y.append(tmp_y[0])
        plt.plot(tmp_x, tmp_y, c=c)


# ------------------------------------------------------------------------- #


kolo1 = kolo(1, 1, 4)
print(str(kolo1))
print(kolo1.czywkole(10, 4))

elipsa1 = elipsa(1, 1, 3, 6)
print(str(elipsa1))
print(elipsa1.czywelipsie(3, 10))


# ------------------------------------------------------------------------- #

# config
num_of_points = 200
ran = [-20, 20]
rect_color = 'red'
square_color = 'blue'

# points
points = [Points(randint(ran[0], ran[1]), randint(ran[0], ran[1])) for _ in range(num_of_points)]
points = list(set(points))
points = sorted(points, key=lambda point: point.x)
Points.display_points()

# rectangles
rectangles = Points.get_rectangles()
rectangles = list(set(rectangles))
for rect in rectangles:
    Rect.display_rect(rect, rect_color)

# show results
plt.show()

# ------------------------------------------------------------------------- #

print("# ------------------------------------------------------------------------- #")

# Przyklad z prawidlowym trojkatem
dane = [(61 / 29, 7 / 29), (0, 11 / 2), (1, -1 / 5), (0, 0)]

# Przyklad z punktem wewnatrz trojkata
# dane = [(11, -1), (10, 12), (-1, 11), (0, 0)]

# Przyklad z przyprostokatnymi prostopadlymi do osi
# dane = [(0, 0), (0, 10), (10, 0)]

if trojkat.sprawdzenie_plaszyczny(dane):
    print("Istnieje taki trojkat!")
else:
    print("Nie istnieje taki trojkat!")
