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

	#iridTexture   = pygame.image.load("textures/iridescent_tex.jpg")
	#scalyTexture  = pygame.image.load("textures/scale_tex.jpg")
	#spralTexture  = pygame.image.load("textures/spratlite_tex.png")
	#metalTexture  = pygame.image.load("textures/metalex.jpg")

	#tridTexture = pygame.image.load("textures/metalex.jpg")

	# --------------------------------------- Creacion de materiales ---------------------------------------
	green = Material(diffuse=(0, 1, 0), spec = 32, Ks = 0.1)
	yellow = Material(diffuse=(1, 1, 0), spec = 64, Ks = 0.2)
	red = Material(diffuse=(1, 0, 0), spec = 32, Ks = 0.1)
	blue = Material(diffuse=(0, 0, 1), spec = 32, Ks = 0.1)
	xd = Material(diffuse=(0,1,1), spec = 32, Ks = 0.1, matType=REFLECTIVE)



	## Opacos
	#scaly = Material(spec = 64, Ks = 0.2, texture = scalyTexture)
	#metalex = Material(spec = 32, Ks = 0.1, texture = metalTexture)

	## Reflectivos
	#spratlite = Material(spec = 64, Ks = 0.2, matType = REFLECTIVE, texture = spralTexture)

	## Transparentes
	#iridescent = Material(diffuse=(0.9, 0.9, 0.9), spec = 128, Ks = 0.2, ior= 1.5, matType = TRANSPARENT, texture = iridTexture)

	# ---------------------------------------- Figuras en la escena ----------------------------------------


	raytracer.scene.append(AABB(position = (0,  -5, -6), size = (8,8,8), material = green))
	raytracer.scene.append(AABB(position = (0,  1, -14), size = (8,8,8), material = yellow))

	raytracer.scene.append(Sphere(position = [-5,2,-10], radius = 1, material = red))
	raytracer.scene.append(Sphere(position = [-5,1.5,-7.5], radius = 1, material = blue))
	raytracer.scene.append(Sphere(position = [-5,1,-5], radius = 1, material = xd))

	raytracer.scene.append(Sphere(position = [5,2,-10], radius = 1, material = red))
	raytracer.scene.append(Sphere(position = [5,1.5,-7.5], radius = 1, material = blue))
	raytracer.scene.append(Sphere(position = [5,1,-5], radius = 1, material = xd))

	#trident = Model(file = 'models/trident.obj', 
	#							translate = (0,0.3,-5),
	#							rotate = (-75,45,10),
	#							material = blue)
	#for triange in trident.triangles:
	#		raytracer.scene.append(triange)

	#raytracer.scene.append(Model(file = 'models/trident.obj', 
	#							translate = (0,0.3,-5),
	#							rotate = (-75,45,10),
	#							material = blue))


	
	raytracer.scene.append(AABB(position = (0, -1, -4), size = (1,1,1), material = yellow))

	raytracer.scene.append(Disk(position=(0,2,-9.5), normal=(0,0,1), radius = 2, material= xd))

	#raytracer.scene.append(Triangle(v0=[-1.2, -1, -2],
	#							 v1=[ 1.2, -1, -2],
	#							 v2=[ 0,  1, -2],
	#							 material = xd))

	# ----------------------------------------- Luces de la escena -----------------------------------------
	raytracer.lights.append(AmbientLight(intensity = 0.1))
	raytracer.lights.append(DirectionalLight(direction = (-1,-1,-1), intensity = 0.5))
	#raytracer.lights.append(DirectionalLight(direction = (1,-1,-1), intensity = 0.5))
	raytracer.lights.append(PointLight(point = (0,2,-4.5), intensity = 25, color = (1,0.2,0)))

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