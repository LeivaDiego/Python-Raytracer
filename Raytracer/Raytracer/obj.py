class Obj(object):
    def __init__(self, filename):

        # Asumiendo que el archivo es un formato .obj
        with open(filename,"r") as file:
            self.lines = file.read().splitlines()
    
        # Se crean los contenedores de los datos del modelo
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        # Por cada linea en el archivo
        for line in self.lines:

            # Si la linea no cuenta con un prefijo y un valor,
            # seguimos a la siguiente linea
            try:
                prefix, value = line.split(" ",1)
            except: # si encuentra una linea vacia, se pasa a la siguiente linea
                continue
            
            # Dependiendo del prefijo, parseamos y guardamos la informacion
            # en el contenedor correcto
            if prefix == "v": # Vertices
                self.vertices.append(list(map(float,value.split(" "))))
            elif prefix == "vt": # Texture coordinates
                self.texcoords.append(list(map(float,value.split(" "))))
            elif prefix == "vn": # Normals
                self.normals.append(list(map(float,value.split(" "))))
            if prefix == "f": # Faces
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])
