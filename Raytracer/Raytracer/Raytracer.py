import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 500
height = 500

pygame.init()

# Creacion de la pantalla de pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

# Instanciar el raytracer
raytracer = Raytracer(screen)

raytracer.environmentMap = pygame.image.load("maps/orbit_map.jpg")

raytracer.rtClearColor(0.25, 0.25, 0.25)

floorTexture = pygame.image.load("textures/floor_tex.jpg")
roofTexture = pygame.image.load("textures/roof_tex.jpg")
wallTexture = pygame.image.load("textures/wall_tex.jpg")
neonTexture = pygame.image.load("textures/neon_tex.jpg")
alienTexture = pygame.image.load("textures/alien_tex.jpg")
corridorTexture = pygame.image.load("textures/corridor_tex.jpg")


# --------------------------------------- Creacion de materiales ---------------------------------------
# con texturas
wall = Material(spec = 5, Ks = 0.1, texture = wallTexture)
floor = Material(spec = 5, Ks = 0.2, texture = floorTexture)
roof = Material(spec = 5, Ks = 0.25, texture = roofTexture)
alien = Material(spec = 32, Ks = 0.8, texture = alienTexture)
neon = Material(spec = 64, Ks = 0.9, texture = neonTexture)
corridor = Material(spec = 64, Ks = 0.9, texture = corridorTexture)


# Reflectivos
mirror = Material(diffuse=(0.6, 0.7, 1), spec = 64, Ks = 0.2, matType = REFLECTIVE)


# ------------------------------------------ Planos en escena ------------------------------------------
raytracer.scene.append(Plane(position = (0,-5,0), normal=(0,1,0), material =  floor))       # Inferior
raytracer.scene.append(Plane(position = (0,5,0), normal=(0,-1,0), material =  roof))        # Superior
raytracer.scene.append(Plane(position = (-5,0,0), normal=(1,0,0), material =  wall))        # Izquierda
raytracer.scene.append(Plane(position = (5,0,0), normal=(-1,0,0), material =  wall))        # Derecha
raytracer.scene.append(Plane(position = (0,0,-25), normal=(0,0,1), material = wall))        # Trasera
raytracer.scene.append(Plane(position = (0,0,50), normal=(0,0,-1), material = corridor))    # Frontal


# ---------------------------------------- Objetos en la escena ----------------------------------------
raytracer.scene.append(AABB(position = (-1,  -1, -6), size = (1.5,1.5,1.5), material = neon))
raytracer.scene.append(AABB(position = (1, -1, -5), size = (1.5,1.5,1.5), material = alien))

raytracer.scene.append(Disk(position=(0,0,-15), normal=(0,0,1), radius = 2.5, material= mirror))


# ----------------------------------------- Luces de la escena -----------------------------------------
raytracer.lights.append(AmbientLight(intensity = 0.7))


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


rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "output.jpg")

pygame.quit()