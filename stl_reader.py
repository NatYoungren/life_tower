import numpy as np
import stl

stl_file = 'assets\Cube_3d_printing_sample.stl'

for i in stl.mesh.Mesh.from_file(stl_file).data:
    print(i)
    print(type(i))