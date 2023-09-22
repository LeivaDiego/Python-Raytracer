import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

# Creacion de la pantalla de pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

# Instanciar el raytracer
raytracer = Raytracer(screen)
raytracer.rtClearColor(0.25, 0.25, 0.25)

# Creacion de materiales
brick = Material(diffuse=(1, 0.4, 0.4), spec = 8, Ks = 0.01)
grass = Material(diffuse=(0.4, 1, 0.4), spec = 32, Ks = 0.1)
water = Material(diffuse=(0.4, 0.4, 1), spec = 256, Ks = 0.2)

# Figuras en la escena
raytracer.scene.append(Sphere(position = (1,1,-5), radius = 0.5, material = grass))
raytracer.scene.append(Sphere(position = (0,0,-7), radius = 2, material = brick))
raytracer.scene.append(Sphere(position = (0.5,-1,-5), radius = 0.3, material = water))

# Luces de la escena
raytracer.lights.append(AmbientLight(intensity=0.1))
#raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.7))
raytracer.lights.append(PointLight(point = (2.5,0,-5), intensity = 1, color = (1,0,1)))


raytracer.rtClear()
raytracer.rtRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()