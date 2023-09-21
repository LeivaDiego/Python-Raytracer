from tokenize import Special
import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 512
height = 512

pygame.init()

# Creacion de la pantalla de pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

# Instanciar el raytracer
raytracer = Raytracer(screen)
raytracer.rtClearColor(0.4, 0.5, 1)

# Creacion de materiales
snow    = Material(diffuse=(0.9, 0.9, 0.9), spec = 2, Ks = 0.04)
carrot  = Material(diffuse=(  1, 0.4,   0), spec = 50, Ks = 0.1)
pebble  = Material(diffuse=(0.1, 0.1, 0.1), spec = 10, Ks = 0.08)
iris    = Material(diffuse=(  1,   1,   1), spec = 250, Ks = 0.2)


# -------------------------------------- Material Testing ---------------------------------------

raytracer.scene.append(Sphere(position = (0,0, -7), radius = 1, material = iris))
#raytracer.scene.append(Sphere(position = (0,0,-7), radius = 1, material = carrot))
#raytracer.scene.append(Sphere(position = (0,0, -7), radius = 1, material = iris))
#raytracer.scene.append(Sphere(position = (0,0, -7), radius = 1, material = pebble))


# --------------------------------------- Escena Snow Man ---------------------------------------
## Cuerpo
#raytracer.scene.append(Sphere(position = (0,-2.55,-10), radius = 2, material = snow))
#raytracer.scene.append(Sphere(position = (0, 0,-10), radius = 1.6, material = snow))
#raytracer.scene.append(Sphere(position = (0, 2.3,-10), radius = 1.2, material = snow))

## Rostro
##   ojos
#raytracer.scene.append(Sphere(position = (-0.5, 2.45,-8.8), radius = 0.2, material = iris))
#raytracer.scene.append(Sphere(position = ( 0.5, 2.45,-8.8), radius = 0.2, material = iris))
#raytracer.scene.append(Sphere(position = (-0.48, 2.42,-8.5), radius = 0.1, material = pebble))
#raytracer.scene.append(Sphere(position = ( 0.48, 2.42,-8.5), radius = 0.1, material = pebble))
##   nariz
#raytracer.scene.append(Sphere(position = (0, 2.25, -8.8), radius = 0.25, material = carrot))
##   sonrisa
#raytracer.scene.append(Sphere(position = (-0.4, 1.8,-9), radius = 0.1, material = pebble))
#raytracer.scene.append(Sphere(position = (-0.15, 1.7,-9), radius = 0.1, material = pebble))
#raytracer.scene.append(Sphere(position = ( 0.15, 1.7,-9), radius = 0.1, material = pebble))
#raytracer.scene.append(Sphere(position = ( 0.4, 1.8,-9), radius = 0.1, material = pebble))

## Botones
#raytracer.scene.append(Sphere(position = (0,-1.8,-8), radius = 0.30, material = pebble))
#raytracer.scene.append(Sphere(position = (0, -0.5,-8), radius = 0.25, material = pebble))
#raytracer.scene.append(Sphere(position = (0, 0.5,-8), radius = 0.20, material = pebble))


# -------------------------------------- Luces de la escena -------------------------------------

raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction = (0,0,-1), intensity = 0.8))
raytracer.lights.append(PointLight(point = (2.5,0,-3), intensity = 1, color = (1,1,0.8)))

# -----------------------------------------------------------------------------------------------


isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                isRunning = False

    raytracer.rtClear()
    raytracer.rtRender()

    pygame.display.flip()

pygame.quit()