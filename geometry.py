import numpy as np


class Geometry_3D: # TODO: Add normals?
    def __init__(self, vertices=[], faces=[]):
        
        self.vertices = np.array(vertices).reshape(-1, 3)
        self.faces = np.array(faces, dtype=int)
        
    def read(self, path):        
        vs = []
        fs = []
        def parse_vertex(line):
            return np.array([float(x) for x in line.split()[1:]])

        def parse_face(line):
            return np.array([int(x) for x in line.split()[1:]])
        
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    vs.append(parse_vertex(line))
                elif line.startswith('f '):
                    fs.append(parse_face(line))
        
        self.vertices = np.array(vs)
        self.faces = np.array(fs) - 1 # Reduces v indices to 0-indexed


def generate_cube():
    vertices = []
    faces = []
    for x in range(2):
        for y in range(2):
            for z in range(2):
                print(len(vertices), [x, y, z])
                vertices.append([x, y, z])

    faces.append([0, 2, 3])
    faces.append([3, 1, 0])
    vertices = np.array(vertices, dtype=float)
    faces = np.array(faces, dtype=int)
    return vertices, faces
    # for f1 in range(6):

def generate_diamond(offset=(0, 0, 0), scale=1, starting_v=0):
    #    1
    #
    # 2 3 4 5
    #
    #    6
    # vertices = [[0.5, 0.5, 1.0],
    #             [0.0, 0.0, 0.5],
    #             [0.0, 1.0, 0.5],
    #             [1.0, 0.0, 0.5],
    #             [1.0, 1.0, 0.5],
    #             [0.5, 0.5, 0.0]]
    
    vertices = [[0.0, 0.0, 0.5],
                [0.0, 0.5, 0.0],
                [-0.5, 0.0, 0.0],
                [0.0, -0.5, 0.0],
                [0.5, 0.0, 0.0],
                [0.0, 0.0, -0.5]]

    vertices = np.array(vertices)
    # print(vertices)

    vertices *= scale
    # print(vertices)
    # print(scale)

    vertices += offset
    
    faces = [[0, 1, 2],
             [0, 2, 3],
             [0, 3, 4],
             [0, 4, 1],
             
             [5, 2, 1],
             [5, 3, 2],
             [5, 4, 3],
             [5, 1, 4],
             ]
    faces = np.array(faces)
    faces += starting_v
    
    return vertices, faces
