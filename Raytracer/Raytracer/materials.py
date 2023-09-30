
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    # Clase que representa el material de un objeto
    # dicta el comportamiento de la luz con la superficie del objeto

    def __init__(self, diffuse = (1,1,1), spec = 1.0, Ks = 0.0, ior = 1.0, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.specular = spec
        self.Ks = Ks # Coeficiente especular
        self.type = matType
        self.texture = texture
        self.ior = ior