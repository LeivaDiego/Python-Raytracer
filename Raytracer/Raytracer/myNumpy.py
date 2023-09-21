from math import isclose, sqrt

def barycentricCoords(A, B, C, P):
    
    # Se saca el area de los subtriangulos y del triangulo
    # mayor usando el Shoelace Theorem, una formula que permite
    # sacar el area de un poligono de cualquier cantidad de vertices.

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el area del triangulo es 0, retornar nada para
    # prevenir division por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baricentricas dividiendo el 
    # area de cada subtriangulo por el area del triangulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada esta entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son validas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return (-1,-1,-1)


def matrix_multiplier(matrixA, matrixB):
    # Multiplica dos matrices y devuelve el resultado
    # matrixA: Primera matriz (fila x columna)
    # matrixB: Segunda matriz (fila x columna)
    # Retorna: Resultado de la multiplicacion (fila x columna)

    # Obtener el numero de filas y columnas de cada matriz
    rowsA = len(matrixA)
    colsA = len(matrixA[0])
    rowsB = len(matrixB)
    colsB = len(matrixB[0])

    # Verificar si las matrices son multiplicables
    if colsA != rowsB:
        raise ValueError("Las dimensiones de las matrices no permiten su multiplicacion.")

    # Crear una matriz vacia para almacenar el resultado
    matrixC = [[0 for _ in range(colsB)] for _ in range(rowsA)]

    # Realizar la multiplicacion de matrices
    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                matrixC[i][j] += matrixA[i][k] * matrixB[k][j]
    return matrixC


def matrix_vector_multiplier(matrix, vector):
    # Multiplica una matriz por un vector y devuelve el resultado
    # matrix: Matriz de multiplicacion (fila x columna)
    # vector: Vector de multiplicacion (1 x columna)
    # Retorna: Resultado de la multiplicacion (1 x columna)

    # Obtener el numero de filas y columnas de la matriz y el vector
    rows = len(matrix)
    cols = len(matrix[0])
    size = len(vector)

    # Verificar si la matriz y el vector son multiplicables
    if cols != size:
        raise ValueError("Las dimensiones de la matriz y el vector no permiten su multiplicacion.")

    # Crear un vector vacio para almacenar resultados
    newVector = [0 for _ in range(rows)]

    # Realizar la multiplicacion de matriz por vector
    for i in range(rows):
        for j in range(cols):
            newVector[i] += matrix[i][j] * vector[j]
    return newVector


def identity_matrix(n):
    # Genera una matriz identidad de tamaño n x n
    # n: Tamano de la matriz
    # Retorna: Matriz identidad n x n
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def inverse_matrix(matrix):
    # Calcula la matriz inversa usando eliminacion gaussiana
    # matrix: Matriz original a invertir (fila x columna)
    # Retorna: Matriz inversa resultante (fila x columna)

    n = len(matrix)
    # Crear una matriz aumentada con la matriz original y la matriz identidad
    augmented_matrix = [row + identity_matrix(n)[i] for i, row in enumerate(matrix)]

    # Realizar la eliminacion gaussiana para calcular la inversa
    for i in range(n):
        pivot = augmented_matrix[i][i]
        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    # Extraer la parte de la inversa de la matriz aumentada
    inverse = [row[n:] for row in augmented_matrix]
    return inverse


def cross_product(vecA, vecB):
    # Calcula el producto cruz entre dos vectores en 3D
    # vecA: Primer vector (3 componentes)
    # vecB: Segundo vector (3 componentes)
    # Retorna: Vector resultante del producto cruz (3 componentes)

    # Verificar si los vectores son de 3 componentes
    if len(vecA) != 3 or len(vecB) != 3:
        raise ValueError("Los vectores deben ser de 3 componentes.")
    
    # Calcular el producto cruz entre dos vectores en 3D
    result = [
        vecA[1] * vecB[2] - vecA[2] * vecB[1],
        vecA[2] * vecB[0] - vecA[0] * vecB[2],
        vecA[0] * vecB[1] - vecA[1] * vecB[0]
    ]
    return result


def vector_normalize(vector):
    # Normaliza un vector dividiendo cada componente por su magnitud
    # vector: Vector a normalizar
    # Retorna: Vector normalizado

    # Calcular la magnitud del vector
    magnitude = sqrt(sum(component ** 2 for component in vector))
    # Normalizar el vector dividiendo cada componente por la magnitud
    normalized_vector = [component / magnitude for component in vector]
    return normalized_vector

def vector_normal(vector):
    # Obtiene la normal de un vector
    # vector: Vector a sacar su normal
    # Retorna: la normal del vector

    # Calcular la magnitud del vector
    magnitude = sqrt(sum(component ** 2 for component in vector))

    return magnitude

def subtract_vector(vectorA, vectorB):
    # Resta dos vectores componente a componente
    # vectorA: Vector minuendo
    # vectorB: Vector sustraendo
    # Retorna: Vector resultante de la resta

    # Verificar si los vectores tienen la misma longitud
    if len(vectorA) != len(vectorB):
        raise ValueError("Los vectores deben tener la misma longitud.")
    # Restar componente a componente los vectores
    return [a - b for a, b in zip(vectorA, vectorB)]


def dot_product(A, B):
    # Clacula el producto punto entre 2 vectores

    if len(A) != len(B):
        raise ValueError("los vectores deben tener la misma longitud")

    result = 0
    for i in range(len(A)):
        result += A[i] * B[i]
    
    return result


def reflectVector(normal, direction):
    # Calcula el reflejo de un vector

    # obtiene el producto punto de la normal y la direccion
    reflect = 2 * dot_product(normal, direction)
    # multiplica el resultado por la normal
    reflect = [reflect * normal[i] for i in range(3)]
    # resta la direccion al resultado
    reflect = subtract_vector(reflect, direction)
    # normaliza el resultado
    reflect = vector_normalize(reflect)

    return reflect