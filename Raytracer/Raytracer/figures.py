import numpy as np

class Shape(object):

    def __init__(self, position):
        self.position = position


    def ray_intersect(self, origin, direction):
        # Verifica si un rayo interseca con una figura
        # dado su origen y su direccion
        return False


class Sphere(Shape):

    def __init__(self, position, radius):
        self.radius = radius
        super().__init__(position)


    def ray_intersect(self, origin, direction):
        # Propia funcion de interceccion de rayos para la esfera
        L = np.subtract(self.position, origin)
        lengthL = np.linalg.norm(L)
        tca = np.dot(L, direction)
        d = (lengthL**2 - tca **2) ** 0.5

        if d > self.radius:
            return False

        thc = (self.radius **2 - d **4) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return False

        return True