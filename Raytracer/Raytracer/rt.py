from math import pi, tan, atan2, acos
from materials import *
from myNumpy import dot_product, fresnel, refractVector, totalInternalReflection, vector_normalize, add_vector,subtract_vector, reflectVector, vector_scalar_mult
import pygame
import random

# Veces que se puede reflejar un rayo
MAX_RECURSION_DEPTH = 3


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

        self.environmentMap = None


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


    def rtCastRay(self, origin, direction, sceneObj = None, recursion = 0):
        # Verifica el contacto de los rayos con cada objeto

        if recursion >= MAX_RECURSION_DEPTH:
            return None

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


    def rtRayColor(self, intercept, rayDirection, recursion = 0):

        if intercept == None:
            if self.environmentMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2 * pi) + 0.5) * self.environmentMap.get_width()
                y = acos(rayDirection[1]) / pi * self.environmentMap.get_height()

                environmentColor = self.environmentMap.get_at((int(x),int(y)))

                return [environmentColor[i] / 255 for i in range(3)]

            else:
                return None

        # Modelo de reflexion Phong
        # LightColor = AmbientIntensity + Diffuse + Specular
        # FinalColor = SurfaceColor * LightColor

        # Tipo de material
        material = intercept.obj.material

        # Color de superficie
        surfaceColor = material.diffuse

        if material.texture and intercept.texcoords:
            tX = intercept.texcoords[0] * material.texture.get_width()
            tY = intercept.texcoords[1] * material.texture.get_height()
            
            texColor = material.texture.get_at((int(tX),int(tY)))
            texColor = [i / 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]


        #Color del reflejo
        reflectColor = [0,0,0]

        # Color de refraccion
        refractColor = [0,0,0]

        # Color de luces
        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specularColor =[0,0,0]

        finalColor = [0,0,0]

        # Para superficie Opaca 
        if material.type == OPAQUE:
            
            for light in self.lights:
                if light.type == "Ambient":
                    ambientColor = [ambientColor[i] + light.getLightColor()[i] for i in range(3)]
                else:
                               
                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]
                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = vector_normalize(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        diffuseColor = [diffuseColor[i] + light.getDiffuseColor(intercept)[i] for i in range(3)]
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]


        # Para superficie reflectiva
        elif material.type == REFLECTIVE:
            reflect = reflectVector(intercept.normal, [i * -1 for i in rayDirection])
            refractIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            # Calcular el color reflejado
            reflectColor = self.rtRayColor(refractIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.type != "Ambient":

                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]

                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = vector_normalize(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]

        # Para superficie refractiva (transparente)
        elif material.type == TRANSPARENT:
            # Revisar si esta afuera
            outside = dot_product(rayDirection, intercept.normal) < 0
            # Agregar un margen de error
            bias = vector_scalar_mult(0.0001, intercept.normal)

            # Generacion de rayos de refleccion
            reflect = reflectVector(intercept.normal, vector_scalar_mult(-1, rayDirection))
            reflectOrigin = add_vector(intercept.point, bias) if outside else subtract_vector(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrigin, reflect, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)

            # Calcular la especularidad del material
            for light in self.lights:
                if light.type != "Ambient":

                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]

                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = vector_normalize(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]


            # Generacion de rayos de refraccion si no hay refleccion interna total
            if not totalInternalReflection(intercept.normal, rayDirection, 1.0, material.ior):
                refract = refractVector(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrigin = subtract_vector(intercept.point, bias) if outside else add_vector(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrigin, refract, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion + 1)

                # Usando Fresnel se determina la intensidad de la refleccion y refraccion
                Kr, Kt = fresnel(intercept.normal, rayDirection, 1.0, material.ior)
                reflectColor = vector_scalar_mult(Kr, reflectColor)
                refractColor = vector_scalar_mult(Kt, refractColor)


        # Obtencion del color final en la superficie
        lightColor = [ambientColor[i] + diffuseColor[i] + specularColor[i] + reflectColor[i] + refractColor[i] for i in range(3)]
        finalColor = [min(1, surfaceColor[i] * lightColor[i]) for i in range(3)]

        return finalColor



    def rtRender(self):
        # Renderiza en la pantalla
        # Generar los rayos para cada pixel de la pantalla

        indeces = [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indeces)

        for i, j in indeces:
            x = i + self.vpX
            y = j + self.vpY

            # Pasar de coordenadas de ventana a
            # coordenadas NDC, coordenadas normalizadas (rango de -1 a 1)
            if (0 <= x < self.width) and (0 <= y < self.height):
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1
                    
                Px *= self.rightEdge
                Py *= self.topEdge

                # Crear un rayo
                direction = [Px, Py, -self.nearPlane]
                direction = vector_normalize(direction)

                intercept =  self.rtCastRay(self.camPosition, direction)
                    
                rayColor = self.rtRayColor(intercept, direction)
                
                if rayColor:
                    self.rtPoint(x,y, rayColor)
                    pygame.display.flip()