from turtle import color
import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

def main():
	width = 100
	height = 100

	pygame.init()

	# Creacion de la pantalla de pygame
	screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
	screen.set_alpha(None)

	# Instanciar el raytracer
	raytracer = Raytracer(screen)

	raytracer.environmentMap = pygame.image.load("maps/space.jpg")

	raytracer.rtClearColor(0.25, 0.25, 0.25)

	# ---------------------------------------- Creacion de Texturas ----------------------------------------

	
	planet1Texture = pygame.image.load("textures/planet1.jpg")
	planet2Texture = pygame.image.load("textures/planet2.jpg")
	planet3Texture = pygame.image.load("textures/planet3.jpg")
	planet4Texture = pygame.image.load("textures/planet4.jpg")

	floorTexture = pygame.image.load("textures/floor.jpg")
	titaTexture = pygame.image.load("textures/titanium.jpg")

	energyTexture  = pygame.image.load("textures/energy.jpeg")
	iridTexture	= pygame.image.load("textures/iridescent.jpg")

	# --------------------------------------- Creacion de materiales ---------------------------------------

	# Opacos
	planet1 = Material(spec = 2,  Ks = 0.04, texture = planet1Texture)
	planet2 = Material(spec = 2,  Ks = 0.04, texture = planet2Texture)
	planet3 = Material(spec = 2,  Ks = 0.04, texture = planet3Texture)
	planet4 = Material(spec = 2,  Ks = 0.04, texture = planet4Texture)

	pilar = Material(spec = 64, Ks = 0.25, texture = titaTexture)
	gold = Material(diffuse=(1, 1, 1), spec = 10, Ks = 0.01)

	# Reflectivos
	floor = Material(spec = 256,  Ks = 0.6, matType = REFLECTIVE, texture = floorTexture)
	base  = Material(diffuse = (0.2,0.8,0.8), spec = 256, Ks = 0.6, matType = REFLECTIVE)

	# Transparentes
	portal = Material(spec = 100, Ks = 0.8, ior = 2.5, matType = TRANSPARENT, texture = energyTexture)
	iridescent = Material(diffuse=(0.9, 0.9, 0.9), spec = 128, Ks = 0.2, ior= 0.8, matType = TRANSPARENT, texture = iridTexture) 

	# ---------------------------------------- Figuras en la escena ----------------------------------------
	# Suelo
	raytracer.scene.append(AABB(position = (0,  -1.5, -6.5), size = (13,0.1,10), material = floor))

	## Base circular
	raytracer.scene.append(Disk(position=(0,-1.4,-5), normal=(0,1,0), radius = 2, material = base))
	raytracer.scene.append(Disk(position=(0,-1.35,-5), normal=(0,1,0), radius = 1.75, material = base))
	raytracer.scene.append(Disk(position=(0,-1.3,-5), normal=(0,1,0), radius = 1.5, material = base))
	raytracer.scene.append(Disk(position=(0,-1.25,-5), normal=(0,1,0), radius = 1.25, material = base))
	raytracer.scene.append(Disk(position=(0,-1.2,-5), normal=(0,1,0), radius = 1, material = base))

	# Portal
	raytracer.scene.append(AABB(position = (0,  2, -11), size = (4,4,4), material = portal))

	# Planetas
	raytracer.scene.append(Sphere(position = [7,1,-18], radius = 2.5, material = planet2))
	raytracer.scene.append(Sphere(position = [10,9,-22], radius = 2, material = planet3))
	raytracer.scene.append(Sphere(position = [10,8,-30], radius = 1, material = planet1))
	raytracer.scene.append(Sphere(position = [-8,8,-35], radius = 10, material = planet4))

	# Pilares
	raytracer.scene.append(AABB(position = (-2.5,-1,  -8), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (-3,  -1,  -7), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (-5,  -1,  -9), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (-2.5,-1, -10), size = (0.2,1,0.2), material = pilar))

	raytracer.scene.append(AABB(position = (2.5,-1,  -8), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (3,  -1,  -7), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (5,  -1,  -9), size = (0.2,1,0.2), material = pilar))
	raytracer.scene.append(AABB(position = (2.5,-1, -10), size = (0.2,1,0.2), material = pilar))

	# Tridente
	raytracer.scene.append(Model(file = 'models/trident.obj', 
								translate = (0, -0.2, -5),
								rotate = (270, 0, 0),
								scale = (0.4, 0.01, 0.5),
								material = gold))

	raytracer.scene.append(Triangle(v0=[-0.3, -1, -2],
								 v1=[ 0.3, -1, -2],
								 v2=[ 0,  -0.5, -2.1],
								 material = iridescent))

	raytracer.scene.append(Triangle(v0=[0.5, -1, -2.1],
								 v1=[ 1.1, -1, -2.6],
								 v2=[ 0.8,  -0.4, -2.5],
								 material = iridescent))

	raytracer.scene.append(Triangle(v0=[-0.5, -1, -2.1],
								v1=[ -1.1, -1, -2.6],
								v2=[ -0.8,  -0.4, -2.5],
								material = iridescent))


	# ----------------------------------------- Luces de la escena -----------------------------------------
	raytracer.lights.append(AmbientLight(intensity = 0.1))
	raytracer.lights.append(DirectionalLight(direction = (0,-1,-1), intensity = 0.5))
	raytracer.lights.append(PointLight(point = (0,-0.85,-5.15), intensity = 10, color = (1,1,1)))
	raytracer.lights.append(PointLight(point = (-20,5,-20), intensity = 50, color = (1,0.3,0)))
	raytracer.lights.append(PointLight(point = (15,6,-15), intensity = 20, color = (0,0.7,1)))
	raytracer.lights.append(PointLight(point = (0,2.45,-8), intensity = 5, color = (0,1,1)))

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

if __name__ == '__main__':
	main()