

class Light(object):
    # Clase que representa una luz

    def __init__(self, intensity = 1, color = (1,1,1), light_type = "None"):
        self.intensity = intensity
        self.color = color
        self.type = light_type

class AmbientLight(Light):
    # Clase que representa la luz ambiental

    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color)


class DirectionalLight(Light):
    # Clase que representa la luz direccional
    def __init__(self, direction = (0,-1,0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
        self.direction = direction