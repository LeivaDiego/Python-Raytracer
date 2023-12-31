from myNumpy import add_vector, barycentricCoords, matrix_multiplier, matrix_vector_multiplier, vector_magnitude, dot_product, subtract_vector, vector_normalize, vector_scalar_mult, cross_product
from math import pi, atan2, acos, sin, cos, sqrt
from obj import Obj

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


class BoundingBox:
	def __init__(self, min_corner, max_corner):
		# Instancia la caja delimitadora, dado un vertice minimo y un maximo
		self.corners = [min_corner, max_corner]

	def intersection(self, origin, direction, tmax=float('inf')):
		# Obtiene si un rayo dado golpea la cada delimitadora de un objeto
		tmin = 0.0
		epsilon = 1e-6

		dir_inv = [1.0 / d if d != 0 else float('inf') for d in direction]
		tmin = 0.0
		for d in range(3):
			sign = 1 if dir_inv[d] < 0 else 0
			bmin = self.corners[sign][d]
			bmax = self.corners[not sign][d]
			dmin = (bmin - origin[d]) * dir_inv[d]
			dmax = (bmax - origin[d]) * dir_inv[d]

			# Aplicar el ajuste epsilon
			t1 = min(dmin, dmax) - epsilon
			t2 = max(dmin, dmax) + epsilon

			tmin = max(t1, tmin)
			tmax = min(t2, tmax)
		return tmin < tmax


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

		# Obtener la bounding box del triangulo
		self.bounding_box = self.get_bounding_box()

		super().__init__(v0, material)


	def get_bounding_box(self):
		# Define la caja delimitadora obteniendo minimos y maximos de los vertices del triangulo

		min_corner = [
			min(self.v0[0], self.v1[0], self.v2[0]),
			min(self.v0[1], self.v1[1], self.v2[1]),
			min(self.v0[2], self.v1[2], self.v2[2])
		]
		max_corner = [
			max(self.v0[0], self.v1[0], self.v2[0]),
			max(self.v0[1], self.v1[1], self.v2[1]),
			max(self.v0[2], self.v1[2], self.v2[2])
		]
		return BoundingBox(min_corner, max_corner)


	def ray_intersect(self, origin, direction):
		# Verifica si un rayo golpea al triangulo

		# Si no esta en el bounding box, se descarta
		if not self.bounding_box.intersection(origin, direction):
			return None

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


class Model(Shape):
	# Clase que representa un modelo 3D

	def __init__(self, file, material, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
		self.filename = file
		self.material = material
		self.translate = translate
		self.rotate = rotate
		self.scale = scale
		self.triangles = []
		self.load_model()
		self.bounding_box = self.get_bounding_box()
	
	def get_bounding_box(self):
		# Obtiene la caja delimitadora dadas las cajas 
		# minimas y maximas de los triangulos que lo componen
		
		if not self.triangles:
			return None

		min_corner = list(self.triangles[0].bounding_box.corners[0])
		max_corner = list(self.triangles[0].bounding_box.corners[1])

		for triangle in self.triangles[1:]:
			for d in range(3):
				min_corner[d] = min(min_corner[d], triangle.bounding_box.corners[0][d])
				max_corner[d] = max(max_corner[d], triangle.bounding_box.corners[1][d])

		return BoundingBox(min_corner, max_corner)


	def load_model(self):
		# Carga la informacion del modelo del archivo .obj para su procesamiento

		obj = Obj(self.filename)
		
		# Descomposicion del modelo en triangulos
		for face in obj.faces:
			v0 = obj.vertices[face[0][0] - 1]
			v1 = obj.vertices[face[1][0] - 1]
			v2 = obj.vertices[face[2][0] - 1]
			
			# Obtener matrices de transformacion respectivas 
			T = Transform.translation(*self.translate)
			Rx = Transform.rotation_x(self.rotate[0])
			Ry = Transform.rotation_y(self.rotate[1])
			Rz = Transform.rotation_z(self.rotate[2])
			R = matrix_multiplier(matrix_multiplier(Rx, Ry), Rz)

			S = Transform.scale(*self.scale)

			transformation_matrix = matrix_multiplier((matrix_multiplier(T, R)), S)
			
			# Aplicar las transformaciones correspondientes
			v0 = matrix_vector_multiplier(transformation_matrix, v0 + [1]) [:3]
			v1 = matrix_vector_multiplier(transformation_matrix, v1 + [1]) [:3]
			v2 = matrix_vector_multiplier(transformation_matrix, v2 + [1]) [:3]
		
			# Creacion de una instancia de Triangle
			self.triangles.append(Triangle(v0, v1, v2, self.material))

	def ray_intersect(self, origin, direction):
		# Verifica que el rayo golpee la caja delimitadora del modelo, 
		# de lo contrario se omite, y no se prueba con sus poligonos
		if not self.bounding_box.intersection(origin, direction):
			return None

		for triangle in self.triangles:
			intersect = triangle.ray_intersect(origin, direction)
			if intersect is not None:
				return intersect  # Retorna la primera interseccion encontrada

		return None  # Retorna None si no hay intersecciones
		
	
class Transform:
	# Clase que representa las matrices de transformaciones basicas de un objeto

	@staticmethod
	def translation(tx, ty, tz):
		# Matrix de traslacion
		return [[1, 0, 0, tx],
				[0, 1, 0, ty],
				[0, 0, 1, tz],
				[0, 0, 0, 1]]

	@staticmethod
	def scale(sx, sy, sz):
		# Matriz de escala
		return [[sx, 0, 0, 0],
				[0, sy, 0, 0],
				[0, 0, sz, 0],
				[0, 0, 0, 1]]

	@staticmethod
	def rotation_x(pitch):

		pitch *= pi/180

		# Matriz de rotacion en eje X
		pitchMat = [[1,0,0,0],
					[0,cos(pitch),-sin(pitch),0],
					[0,sin(pitch),cos(pitch),0],
					[0,0,0,1]]

		return pitchMat

	@staticmethod
	def rotation_y(yaw):

		yaw *= pi/180

		# Matriz de rotacion en eje Y
		yawMat = [[cos(yaw),0,sin(yaw),0],
					[0,1,0,0],
					[-sin(yaw),0,cos(yaw),0],
					[0,0,0,1]]

		return yawMat

	@staticmethod
	def rotation_z(roll):

		roll *= pi/180

		# Matriz de rotacion en eje Z
		rollMat = [[cos(roll),-sin(roll),0,0],
				   [sin(roll),cos(roll),0,0],
				   [0,0,1,0],
				   [0,0,0,1]]

		return rollMat


class Cylinder(Shape):
	def __init__(self, position, radius, height, material):
		self.radius = radius
		self.height = height
		super().__init__(position, material)


	def ray_intersect(self, origin, direction):
		# Variables auxiliares
		dx, dy, dz = direction
		ox, oy, oz = origin
		cx, cy, cz = self.position[0], self.position[1] - self.height / 2, self.position[2]

		# Intersección con el cuerpo lateral del cilindro
		a = dx**2 + dz**2
		b = 2 * ((ox - cx) * dx + (oz - cz) * dz)
		c = (ox - cx)**2 + (oz - cz)**2 - self.radius**2

		discriminant = b**2 - 4*a*c
		if discriminant >= 0:
			sqrt_discriminant = sqrt(discriminant)
			for t in [(-b - sqrt_discriminant) / (2*a), (-b + sqrt_discriminant) / (2*a)]:
				y_intersect = oy + t * dy
				if cy <= y_intersect <= cy + self.height:
					P = [ox + t * dx, oy + t * dy, oz + t * dz]
					normal = [(P[0] - cx) / self.radius, 0, (P[2] - cz) / self.radius]
					u = (atan2(normal[2], normal[0]) / (2 * pi) + 0.5)
					v = (y_intersect - cy) / self.height
					return Intercept(t, P, normal, self, (u, v))

		return None