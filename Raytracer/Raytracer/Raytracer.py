import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

def main():
	width = 192
	height = 108

	pygame.init()

	# Creacion de la pantalla de pygame
	screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
	screen.set_alpha(None)

	# Instanciar el raytracer
	raytracer = Raytracer(screen)

	raytracer.environmentMap = pygame.image.load("maps/nebula.jpg")

	raytracer.rtClearColor(0.25, 0.25, 0.25)

	# ---------------------------------------- Creacion de Texturas ----------------------------------------

	iridTexture	= pygame.image.load("textures/iridescent_tex.jpg")
	planet1Texture = pygame.image.load("textures/planet1.jpg")
	planet2Texture = pygame.image.load("textures/planet2.jpg")
	planet3Texture = pygame.image.load("textures/planet3.jpg")
	planet4Texture  = pygame.image.load("textures/scale_tex.jpg")
	hexTexture	= pygame.image.load("textures/hex.png")
	floorTexture	= pygame.image.load("textures/floor.jpg")
	crystalTexture	= pygame.image.load("textures/crystal.jpg")
	energyTexture  = pygame.image.load("textures/energy.jpg")
	metalexTexture = pygame.image.load("textures/metalex.jpg")

	# --------------------------------------- Creacion de materiales ---------------------------------------

	# Opacos
	scalyPlanet = Material(spec = 64, Ks = 0.2, texture = planet4Texture)
	planet1 = Material(spec = 32, Ks = 0.15, texture = planet1Texture)
	planet2 = Material(spec = 32, Ks = 0.15, texture = planet2Texture)
	metallicPlanet = Material(spec = 128, Ks = 0.25, texture = metalexTexture)
	podium = Material(diffuse=(1, 0.7, 0.2),spec = 128, Ks = 0.25, texture = energyTexture)
	gold = Material(diffuse=(0.7, 1, 0), spec = 64, Ks = 0.2)

	# Reflectivos
	floor = Material(spec = 64, Ks = 0.2, matType = REFLECTIVE, texture = floorTexture)
	portal = Material(diffuse = (0.6, 0.2, 1), spec = 128, Ks = 0.25, matType = REFLECTIVE)
	planetHex = Material(spec = 32, Ks = 0.1, matType = REFLECTIVE, texture = hexTexture)

	# Transparentes
	iridescent = Material(diffuse=(0.9, 0.9, 0.9), spec = 128, Ks = 0.2, ior= 0.8, matType = TRANSPARENT, texture = iridTexture)
	crystal = Material(diffuse=(0.6, 1, 0.8), spec = 130, Ks = 0.25, ior= 0.5, matType = TRANSPARENT, texture = crystalTexture)
	planet3 = Material(spec = 130, Ks = 0.25, ior= 1.0, matType = TRANSPARENT, texture = planet3Texture)

	# ---------------------------------------- Figuras en la escena ----------------------------------------


	raytracer.scene.append(AABB(position = (0,  -5, -6), size = (8,8,8), material = floor))
	raytracer.scene.append(AABB(position = (0,  1, -14), size = (8,8,8), material = crystal))

	raytracer.scene.append(Sphere(position = [-5,2,-10], radius = 1, material = scalyPlanet))
	raytracer.scene.append(Sphere(position = [-5,1.5,-7.5], radius = 1, material = planet3))
	raytracer.scene.append(Sphere(position = [-5,1,-5], radius = 1, material = planet1))

	raytracer.scene.append(Sphere(position = [5,2,-10], radius = 1, material = planet2))
	raytracer.scene.append(Sphere(position = [5,1.5,-7.5], radius = 1, material = planetHex))
	raytracer.scene.append(Sphere(position = [5,1,-5], radius = 1, material = metallicPlanet))

	raytracer.scene.append(Model(file = 'models/trident.obj', 
								translate = (0,0.3,-5),
								rotate = (-75,45,10),
								material = gold))


	raytracer.scene.append(AABB(position = (0, -1, -4), size = (1,1,1), material = podium))

	raytracer.scene.append(Disk(position=(0,2,-9.5), normal=(0,0,1), radius = 2, material= portal))

	raytracer.scene.append(Triangle(v0=[-1.2, -1, -2],
								 v1=[ 1.2, -1, -2],
								 v2=[ 0,  1, -2],
								 material = iridescent))

	# ----------------------------------------- Luces de la escena -----------------------------------------
	raytracer.lights.append(AmbientLight(intensity = 0.1))
	raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.5))
	raytracer.lights.append(DirectionalLight(direction = (1,-1,-1), intensity = 0.5))
	raytracer.lights.append(PointLight(point = (0,2,-4.5), intensity = 5, color = (0.5,0.2,0.9)))

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