import numpy as np


# class Object: # TODO: Add normals?
#     def __init__(self, vertices, faces):
#         self.vertices = vertices
#         self.faces = faces

class ObjReader:
    def __init__(self, path):
        self.path = path
        self.vertices = []
        self.faces = []
        self.read()
    
    def read(self, path=None):
        if path is None:
            path = self.path
        
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    self.vertices.append(self.parse_vertex(line))
                elif line.startswith('f '):
                    self.faces.append(self.parse_face(line))
        
        self.vertices = np.array(self.vertices)
        self.faces = np.array(self.faces) - 1 # Reduces v indices to 0-indexed
        
    def parse_vertex(self, line):
        return np.array([float(x) for x in line.split()[1:]])

    def parse_face(self, line):
        return np.array([int(x) for x in line.split()[1:]])
    
    # def get_object(self):
    #     return Object(self.vertices, self.faces)