from myNumpy import add_vector, vector_magnitude, dot_product, subtract_vector, vector_normalize, vector_scalar_mult, cross_product
from math import pi, atan2, acos
from obj import Obj
import numpy as np

class Intercept(object):
	def __init__(self, distance, point, normal, obj, texcoords):
		self.distance = distance
		self.point = point
		self.normal = normal
		self.obj = obj
		self.texcoords = texcoords



class Shape(object):

	def __init__(self, position, material):
		self.position = position
		self.material = material

	def ray_intersect(self, origin, direction):
		# Verifica si un rayo interseca con una figura
		# dado su origen y su direccion
		return None


class Sphere(Shape):
	# Representacion de una esfera

	def __init__(self, position, radius, material):
		self.radius = radius
		super().__init__(position, material)


	def ray_intersect(self, origin, direction):
		# Propia funcion de interseccion de rayos para la esfera

		L = subtract_vector(self.position, origin)
		lengthL = vector_magnitude(L)
		tca = dot_product(L, direction)
		d = (lengthL**2 - tca **2) ** 0.5

		if d > self.radius:
			return None

		thc = (self.radius ** 2 - d ** 2) ** 0.5

		t0 = tca - thc
		t1 = tca + thc

		if t0 < 0:
			t0 = t1

		if t0 < 0:
			return None
		
		#  P = O + D *t0 
		D = vector_scalar_mult(t0,direction)
		P = add_vector(origin, D)
		point_normal = subtract_vector(P, self.position)
		point_normal = vector_normalize(point_normal)

		u = atan2(point_normal[2], point_normal[0]) / (2 * pi) + 0.5
		v = acos(point_normal[1]) / pi

		return Intercept(distance = t0,
						 point = P,
						 normal = point_normal,
						 obj = self,
						 texcoords = (u,v))


class Plane(Shape):
	# Representacion de un plano infinito

	def __init__(self, position, normal, material):
		self.normal = normal

		# Generar los vectores UV 
		# Revisar si la normal no esta alineada al eje Z
		if abs(self.normal[2]) < 0.999:
			self.u_vector = vector_normalize(cross_product(self.normal, (0,0,1)))
		else:
			self.u_vector = vector_normalize(cross_product(self.normal, (0,1,0)))

		self.v_vector = vector_normalize(cross_product(self.normal, self.u_vector))
		self.v_vector = vector_scalar_mult(-1, self.v_vector)

		super().__init__(position, material)


	def ray_intersect(self, origin, direction):
		# Distancia  = ((posiscion plano - origen rayo) o normal) / (direccion rayo o normal)

		denom = dot_product(direction, self.normal)

		if abs(denom) <= 0.0001:
			return None

		num = dot_product(subtract_vector(self.position, origin), self.normal)
		
		t = num / denom

		if t < 0:
			return None

		#  P = O + D *t0
		D = vector_scalar_mult(t,direction)
		P = add_vector(origin, D)

		# Repeticion cada 10n unidades de la textura
		repeat = 0.1

		# Obtener uv's de textura
		u = dot_product(subtract_vector(P, self.position), self.u_vector) * repeat % 1
		v = dot_product(subtract_vector(P, self.position), self.v_vector) * repeat % 1

		return Intercept(distance = t,
						 point = P,
						 normal = self.normal,
						 obj = self,
						 texcoords = (u,v))


class Disk(Plane):
	# Clase que representa un disco

	def __init__(self, position, normal, radius, material):
		self.radius = radius
		super().__init__(position, normal, material)


	def ray_intersect(self, origin, direction):
		planeIntersect = super().ray_intersect(origin, direction)
		
		if planeIntersect is None:
			return None

		contactVector = subtract_vector(planeIntersect.point, self.position)
		contactDistance = vector_magnitude(contactVector)

		if contactDistance > self.radius:
			return None

		return Intercept(distance = planeIntersect.distance,
						 point = planeIntersect.point,
						 normal = self.normal,
						 obj = self,
						 texcoords = None)


class AABB(Shape):
	# Clase que representa un Axis Aligned Bounding Box

	def __init__(self, position, size, material):
		super().__init__(position, material)

		self.planes = []
		self.size = size

		leftPlane =    Plane(add_vector(self.position, (-size[0] / 2,0,0)), (-1,0,0), material)
		rightPlane =   Plane(add_vector(self.position, ( size[0] / 2,0,0)), ( 1,0,0), material)
					  
		bottomPlane =  Plane(add_vector(self.position, (0,-size[1] / 2,0)), (0,-1,0), material)
		topPlane = 	   Plane(add_vector(self.position, (0, size[1] / 2,0)), (0, 1,0), material)
					   
		backPlane =    Plane(add_vector(self.position, (0,0,-size[2] / 2)), (0,0,-1), material)
		frontPlane =   Plane(add_vector(self.position, (0,0, size[2] / 2)), (0,0, 1), material)

		self.planes.append(leftPlane)
		self.planes.append(rightPlane)
		self.planes.append(bottomPlane)
		self.planes.append(topPlane)
		self.planes.append(backPlane)
		self.planes.append(frontPlane)

		# Bounds
		self.boundsMin = [0,0,0]
		self.boundsMax = [0,0,0]

		self.bias = 0.001

		for i in range(3):
			self.boundsMin[i] = self.position[i] - (self.bias + size[i]/2)
			self.boundsMax[i] = self.position[i] + (self.bias + size[i]/2)
		

	def ray_intersect(self, origin, direction):
		intersect = None
		t = float('inf')

		u = 0
		v = 0

		for plane in self.planes:
			planeIntersect = plane.ray_intersect(origin, direction)

			if planeIntersect is not None:
				
				planePoint = planeIntersect.point

				if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
					if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
						if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
							if planeIntersect.distance < t:
								t = planeIntersect.distance
								intersect = planeIntersect

								# Generacion de las uv's
								if abs(plane.normal[0]) > 0:
									# La cara esta en X, se usa Y y Z para crear las uv's
									u = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)

								elif abs(plane.normal[1]) > 0:
									# La cara esta en Y, se usa X y Z para crear las uv's
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2) 
									v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2) 

								elif abs(plane.normal[2]) > 0:
									# La cara esta en Z, se usa X y Y para crear las uv's
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)

		if intersect is None:
			return None

		return Intercept(distance = t,
						 point = intersect.point,
						 normal = intersect.normal,
						 obj = self,
						 texcoords = (u, v))



class Triangle(Shape):
	# Clase que representa un triangulo en un espacio 3D

	# Referencias: 
	#		- https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/why-are-triangles-useful.html
	# 		- https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution.html
	#		- https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates.html
	#		- https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection.html


	def __init__(self, v0, v1, v2, material):
		# Vertices del triangulo
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2

		# vectores de las aristas del triangulo a partir de los vertices
		self.v0v1 = subtract_vector(self.v1, self.v0)
		self.v0v2 = subtract_vector(self.v2, self.v0)

		# La normal del triangulo a partir del producto cruz normalizado de las aristas
		self.normal = vector_normalize(cross_product(self.v0v1, self.v0v2))

		super().__init__(v0, material)


	def ray_intersect(self, origin, direction):
		# Algoritmo Möller - Trumbore
		pvec = cross_product(direction, self.v0v2)
		det = dot_product(self.v0v1, pvec)
		kEpsilon = 0.001	# valor de tolerancia

		# Si el determinante es cercano a 0, el rayo es paralelo al triangulo
		if abs(det) < kEpsilon:
			return None
		
		# Obtencion de UV's
		
		invDet = 1.0 / det # el inverso del determinante

		tvec = subtract_vector(origin, self.v0) # vector t dado desde el origen de rayo hasta el v0
		
		u = dot_product(tvec, pvec) * invDet

		# si la coordenada U esta fuera del rango [0,1] no interseca con el triangulo
		if u < 0 or u > 1:
			return None
	
		qvec = cross_product(tvec, self.v0v1) # vector q dado por el producto cruz del vector t 
											  # y la primera arista
		
		v = dot_product(direction, qvec) * invDet

		# si la coordenada V esta fuera del rango [0,1] no interseca con el triangulo
		if v < 0 or u + v > 1:
			return None

		# Parametro t: distancia desde el origen hasta el punto de interseccion
		t = dot_product(self.v0v2,qvec) * invDet

		# Si t es negativo, la interseccino esta detras del origen del rayo
		if t < 0:
			return None

		# Punto de interseccion P
		P = add_vector(origin, vector_scalar_mult(t, direction))

		return Intercept(distance=t,
							point=P,
							normal=self.normal,
							obj=self,
							texcoords=(u,v))



class Model:
	# Clase que representa un modelo 3D

	def __init__(self, file, material, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
		self.filename = file
		self.material = material
		self.translate = translate
		self.rotate = rotate
		self.scale = scale
		self.triangles = []
		self.load_model()
		
	def load_model(self):
		# Carga la informacion del modelo del archivo .obj para su procesamiento

		obj = Obj(self.filename)
		
		# Descomposicion del modelo en triangulos
		for face in obj.faces:
			v0 = obj.vertices[face[0][0] - 1]
			v1 = obj.vertices[face[1][0] - 1]
			v2 = obj.vertices[face[2][0] - 1]

			# Obtencion de coordenadas UV para cada vertice
			vt1 = obj.texcoords[face[0][1] - 1] if face[0][1] else None
			vt2 = obj.texcoords[face[1][1] - 1] if face[1][1] else None
			vt3 = obj.texcoords[face[2][1] - 1] if face[2][1] else None
			
			# Aplicar las transformaciones correspondientes
			T = Transform.translation(*self.translate)
			Rx = Transform.rotation_x(self.rotate[0])
			Ry = Transform.rotation_y(self.rotate[1])
			Rz = Transform.rotation_z(self.rotate[2])
			S = Transform.scale(*self.scale)
			transformation_matrix = T @ (Rz @ (Ry @ (Rx @ S)))
			v0 = (transformation_matrix @ np.append(v0, 1))[:3]
			v1 = (transformation_matrix @ np.append(v1, 1))[:3]
			v2 = (transformation_matrix @ np.append(v2, 1))[:3]
			normal = np.cross(v1 - v0, v2 - v0)
			normal = vector_normalize(normal)
		
			# Creacion de una instancia de Triangle
			self.triangles.append(Triangle(v0, v1, v2, self.material))
			


class Transform:
	# Clase que representa las matrices de transformaciones basicas de un objeto

	@staticmethod
	def translation(tx, ty, tz):
		# Matrix de traslacion
		return np.array([
			[1, 0, 0, tx],
			[0, 1, 0, ty],
			[0, 0, 1, tz],
			[0, 0, 0, 1]
		])

	@staticmethod
	def scale(sx, sy, sz):
		# Matriz de escala
		return np.array([
			[sx, 0, 0, 0],
			[0, sy, 0, 0],
			[0, 0, sz, 0],
			[0, 0, 0, 1]
		])

	@staticmethod
	def rotation_x(angle):
		# Matriz de rotacion en eje X
		c = np.cos(np.radians(angle))
		s = np.sin(np.radians(angle))
		return np.array([
			[1, 0, 0, 0],
			[0, c, -s, 0],
			[0, s, c, 0],
			[0, 0, 0, 1]
		])

	@staticmethod
	def rotation_y(angle):
		# Matriz de rotacion en eje Y
		c = np.cos(np.radians(angle))
		s = np.sin(np.radians(angle))
		return np.array([
			[c, 0, s, 0],
			[0, 1, 0, 0],
			[-s, 0, c, 0],
			[0, 0, 0, 1]
		])

	@staticmethod
	def rotation_z(angle):
		# Matriz de rotacion en eje Z
		c = np.cos(np.radians(angle))
		s = np.sin(np.radians(angle))
		return np.array([
			[c, -s, 0, 0],
			[s, c, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		])
