import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 1600
height = 1000

pygame.init()

# Creacion de la pantalla de pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

# Instanciar el raytracer
raytracer = Raytracer(screen)

raytracer.environmentMap = pygame.image.load("maps/containers_map.jpg")

raytracer.rtClearColor(0.25, 0.25, 0.25)

rockTexture = pygame.image.load("textures/rock.jpg")
woodTexture = pygame.image.load("textures/wood.jpg")
holoTexture = pygame.image.load("textures/holographic.jpg")
waterTexture = pygame.image.load("textures/water.jpg")

# --------------------------------------- Creacion de materiales ---------------------------------------
# Opacos
rock = Material(spec = 8, Ks = 0.01, texture = rockTexture)
wood = Material(spec = 10, Ks = 0.08, texture = woodTexture)

# Reflectivos
water = Material( spec = 256, Ks = 0.2, matType = REFLECTIVE, texture = waterTexture)
polished = Material(diffuse=(0.6, 0.6, 0.6), spec = 64, Ks = 0.2, matType = REFLECTIVE)

# Transparentes
holographic = Material(spec = 64, Ks = 0.15, ior = 1.5, matType = TRANSPARENT, texture = holoTexture)
crystal = Material(diffuse=(1, 1, 1), spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT)

# Extra
grass = Material(diffuse=(0.4, 1, 0.4), spec = 32, Ks = 0.1)

# --------------------------------------- Objetos en la escena -----------------------------------------
# opacos
raytracer.scene.append(Sphere(position = (-3, 1.5,-5), radius = 1, material = rock))
raytracer.scene.append(Sphere(position = (-3,-1.5,-5), radius = 1, material = wood))

# reflectivos
raytracer.scene.append(Sphere(position = (0, 1.5,-5), radius = 1, material = water))
raytracer.scene.append(Sphere(position = (0,-1.5,-5), radius = 1, material = polished))

#transparentes
raytracer.scene.append(Sphere(position = (3, 1.5,-5), radius = 1, material = holographic))
raytracer.scene.append(Sphere(position = (3,-1.5,-5), radius = 1, material = crystal))

# Extra
raytracer.scene.append(Sphere(position = (2.8,-1.4,-10), radius = 0.5, material = grass))


# --------------------------------------- Luces de la escena -------------------------------------------
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.9))
#raytracer.lights.append(PointLight(point = (2.5,0,-5), intensity = 1, color = (1,0,1)))


raytracer.rtClear()
raytracer.rtRender()

print("\n Render Time: ", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()