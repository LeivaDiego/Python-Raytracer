from myNumpy import add_vector, vector_normal, dot_product, subtract_vector, vector_normalize, vector_scalar_mult, cross_product
from math import pi, atan2, acos

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
		lengthL = vector_normal(L)
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

		return Intercept(distance = t,
						 point = P,
						 normal = self.normal,
						 obj = self,
						 texcoords = None)


class Disk(Plane):
	# Clase que representa un disco

	def __init__(self, position, normal, radius, material):
		self.radius = radius
		super().__init__(position, normal, material)


	def ray_intersect(self, origin, direction):
		planeIntersect = super().ray_intersect(origin, direction)
		
		if planeIntersect is None:
			return None

		contactDistance = subtract_vector(planeIntersect.point, self.position)
		contactDistance = vector_normal(contactDistance)

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
								if abs(plane.normal[0] > 0):
									# La cara esta en X, se usa Y y Z para crear las uv's
									u = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)
								
								elif abs(plane.normal[1] > 0):
									# La cara esta en Y, se usa X y Z para crear las uv's
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2) 
									v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2) 

								elif abs(plane.normal[2] > 0):
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
	# Clase que representa un triangulo 
	# Referencias de: 
	#				https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/why-are-triangles-useful.html

	def __init__(self, v0, v1, v2, material):
		# Vertices del triangulo
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2

		# Lineas del triangulo
		edge1 = subtract_vector(self.v1, self.v0)
		edge2 = subtract_vector(self.v2, self.v0)

		# La normal
		self.normal = vector_normalize(cross_product(edge1, edge2))

		# El centroide del triangulo
		centroid = [(v0[i] + v1[i] + v2[i]) / 3 for i in range(3)]

		super().__init__(centroid, material)

	def ray_intersect(self, origin, direction):
		NdotRayDirection = dot_product(direction, self.normal)

		# Rayo paralelo al triangulo
		if abs(NdotRayDirection) < 0.0001:
			return None
		
		# Parametro d
		d = - dot_product(self.normal, self.v0)

		# Parametro t
		t = - (dot_product(self.normal, origin) + d) / NdotRayDirection
		
		# El triangulo esta detras de camara
		if t < 0:
			return None
		
		# Punto de interseccion
		P = add_vector(origin, vector_scalar_mult(t, direction))

		# Test Inside-Ouside
		edge0 = subtract_vector(self.v1, self.v0)
		edge1 = subtract_vector(self.v2, self.v1)
		edge2 = subtract_vector(self.v0, self.v2)

		vp0 = subtract_vector(P, self.v0)
		vp1 = subtract_vector(P, self.v1)
		vp2 = subtract_vector(P, self.v2)
		
		# Vector perpendicular al triangulo
		c0 = cross_product(edge0,vp0)
		c1 = cross_product(edge1,vp1)
		c2 = cross_product(edge2,vp2)

		test0 = dot_product(self.normal, c0)
		test1 = dot_product(self.normal, c1)
		test2 = dot_product(self.normal, c2)

		# validar que P toque el triangulo
		if test0 < 0 or test1 < 0 or test2 < 0:
			return None

		return Intercept(distance=t,
							point=P,
							normal=self.normal,
							obj=self,
							texcoords=None)