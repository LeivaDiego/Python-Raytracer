import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 100
height = 100

pygame.init()

# Creacion de la pantalla de pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

# Instanciar el raytracer
raytracer = Raytracer(screen)

raytracer.environmentMap = pygame.image.load("maps/future_map.jpg")

raytracer.rtClearColor(0.25, 0.25, 0.25)

# ---------------------------------------- Creacion de Texturas ----------------------------------------

iridTexture   = pygame.image.load("textures/iridescent_tex.jpg")
scalyTexture  = pygame.image.load("textures/scale_tex.jpg")
spralTexture  = pygame.image.load("textures/spratlite_tex.png")
metalTexture  = pygame.image.load("textures/metalex.jpg")
faceTexture   = pygame.image.load("textures/model.bmp")

# --------------------------------------- Creacion de materiales ---------------------------------------
grass = Material(diffuse=(0.4, 1, 0.4), spec = 32, Ks = 0.1)


# Opacos
scaly = Material(spec = 64, Ks = 0.2, texture = scalyTexture)
metalex = Material(spec = 32, Ks = 0.1, texture = metalTexture)

# Reflectivos
spratlite = Material(spec = 64, Ks = 0.2, matType = REFLECTIVE, texture = spralTexture)

# Transparentes
iridescent = Material(diffuse=(0.9, 0.9, 0.9), spec = 128, Ks = 0.2, ior= 1.5, matType = TRANSPARENT, texture = iridTexture)

# ---------------------------------------- Figuras en la escena ----------------------------------------
cabeza = Model(file = 'models/model.obj', 
			   translate=(0,0,-3), 
			   rotate=(0,90,0), 
			   scale=(1,1,1), 
			   material= grass)

for triangle in cabeza.triangles:
	raytracer.scene.append(triangle)

# ----------------------------------------- Luces de la escena -----------------------------------------
raytracer.lights.append(AmbientLight(intensity = 0.1))
raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.9))
#raytracer.lights.append(PointLight(point = (2.5,0,-4.5), intensity = 100, color = (1,0.2,1)))


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