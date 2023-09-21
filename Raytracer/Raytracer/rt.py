from math import pi, tan
from turtle import color
import numpy as np

from lights import Light

class Raytracer(object):

    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()

        self.scene = [] # Objetos en la escena
        self.lights = [] # luces en la escena
        
        self.camPosition = [0,0,0]
        self.rtViewport(0, 0, self.width, self.height)
        self.rtProjection()
        
        self.rtColor(1,1,1)
        self.rtClearColor(0,0,0)
        self.rtClear()


    def rtViewport(self, posX, posY, width, height):
        # Genera el viewport (parte visible de la imagen)
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height


    def rtProjection(self, fov = 60, n = 0.1):
        # Creacion de la proyeccion

        aspectRatio = self.vpWidth / self.vpHeight

        self.nearPlane = n

        self.topEdge = tan((fov * pi / 180) / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio


    def rtClearColor(self, r,g,b):
        # Reinicia el color
        # Recibe valores de 0 a 1
        self.clearColor = (r*255, g*255, b*255)


    def rtClear(self):
        # Limpia la pantalla
        # Pygame usa valores de color de 0 a 255
        self.screen.fill((self.clearColor[0],
                          self.clearColor[1],
                          self.clearColor[2]))


    def rtColor(self, r, g, b):
        # Establece el color a utilizar
        self.currColor = (r*255, g*255, b*255)

    
    def rtPoint(self, x, y, color = None):
        # Dibuja un punto en pantalla
        y = self.height - y

        # Valida las coordenadas (x,y)
        if (0 <= x < self.width) and (0 <= y <self.height):
            # Valida el color
            if color:
                color = (int(color[0] * 255),
                         int(color[1] * 255),
                         int(color[2] * 255))
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y), self.currColor)


    def rtCastRay(self, origin, direction, sceneObj = None):
        # Verifica el contacto de los rayos con cada objeto
        
        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(origin, direction)
                if intercept:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        
        return hit


    def rtRender(self):
        # Renderiza en la pantalla
        # Generar los rayos para cada pixel de la pantalla
        for x in range(self.vpX, self.vpX + self.vpWidth + 1):
            for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC, coordenadas normalizadas (rango de -1 a 1)
                if (0 <= x < self.width) and (0 <= y < self.height):
                    Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                    Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1
                    
                    Px *= self.rightEdge
                    Py *= self.topEdge
                    direction = [Px, Py, -self.nearPlane]
                    direction = direction / np.linalg.norm(direction)

                    intercept =  self.rtCastRay(self.camPosition, direction)
                    
                    if intercept:
                        # Modelo de reflexion Phong
                        # LightColor = AmbientIntensity + Diffuse + Specular
                        # FinalColor = SurfaceColor * LightColor
                         
                        surfaceColor = intercept.obj.material.diffuse

                        ambientColor = [0,0,0]
                        diffuseColor = [0,0,0]
                        specularColor =[0,0,0]
                        
                        for light in self.lights:
                            if light.type == "Ambient":
                                ambientColor = [ambientColor[i] + light.getLightColor()[i] for i in range(3)]
                            else:
                                shadowIntersect = None

                                if light.type == "Directional":
                                    lightDirection = [i * -1 for i in light.direction]
                                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                                if shadowIntersect == None:
                                    diffuseColor = [diffuseColor[i] + light.getDiffuseColor(intercept)[i] for i in range(3)]
                                    specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]

                                
                        lightColor = [ambientColor[i] + diffuseColor[i] + specularColor[i] for i in range(3)]

                        finalColor = [min(1, surfaceColor[i] * lightColor[i]) for i in range(3)]
                        
                        self.rtPoint(x,y, finalColor)