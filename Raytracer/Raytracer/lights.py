import numpy as np

class Light(object):
    # Clase que representa una luz

    def __init__(self, intensity = 1, color = (1,1,1), light_type = "None"):
        self.intensity = intensity
        self.color = color
        self.type = light_type


    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]


    def getDiffuseColor(self, intercept):
        return self.getLightColor()

    def getSpecularColor(self, intercept, viewPos):
        return None



class AmbientLight(Light):
    # Clase que representa la luz ambiental

    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")



class DirectionalLight(Light):
    # Clase que representa la luz direccional

    def __init__(self, direction = (0,-1,0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
        self.direction = direction / np.linalg.norm(direction)


    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = np.dot(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))

        diffuseColor = [i * intensity for i in self.color]

        return diffuseColor


    
        