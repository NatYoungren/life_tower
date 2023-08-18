# Nathaniel Youngren
# Using: https://youtu.be/D96wb46mjIQ as a guide

import pygame as pg
import numpy as np
from numba import njit
from obj_reader import ObjReader
 


SCREEN_W, SCREEN_H = 800, 600
FOV_V = np.pi / 5
FOV_H = FOV_V * SCREEN_W / SCREEN_H

teapot_file = 'assets/teapot.obj'
obj_reader = ObjReader(teapot_file)
# obj_reader.vertices = np.asarray([[1, 1, 1], [4, 2, 0], [1, 0.5, 3]])
# obj_reader.faces = np.asarray([[0, 1, 2]])

def main():
    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()
    

    surf = pg.surface.Surface((SCREEN_W, SCREEN_H))
    # for v in obj_reader.vertices:
    #     print(v)
    #     pg.draw.circle(screen, (255, 255, 255), (int(v[0]*SCREEN_W/4), int(v[1]*SCREEN_W/4)), 1)
    
    camera = np.array([13, 0.5, 2, 3.3, 0])
    z_order = np.empty(len(obj_reader.faces))

    while running:
        
        elapsed_time = clock.tick() * 0.001
        
        surf.fill((50, 127, 200))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    print('space pressed')
        
        pixel_coords = project_points(obj_reader.vertices, camera)
        sort_faces(obj_reader.vertices, obj_reader.faces, camera, z_order)

        for i in np.argsort(z_order):
            
            if z_order[i] == 9999:
                break
            
            v_is = obj_reader.faces[i]
            triangle = [pixel_coords[index] for index in v_is]
            color = np.abs(obj_reader.vertices[v_is[0]])*45 + 25
            # print(color)
            pg.draw.polygon(surf, color, triangle)
        
        screen.blit(surf, (0, 0))
        pg.display.flip()
        pg.display.set_caption(str(round(1/(elapsed_time+1e-16), 2)) + ' fps : ' + str(camera) )

@njit()
def sort_faces(vertices, faces, camera, z_order):
    for i, face in enumerate(faces):
        
        # Use cross-product to get surface normal
        vet1 = vertices[face[1]] - vertices[face[0]]
        vet2 = vertices[face[2]] - vertices[face[0]]
        
        # backface culling with dot product between normal and camera ray
        normal = np.cross(vet1, vet2)
        normal /= np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        
        camera_ray = vertices[face[0]] - camera[:3]
        
        distance = np.sqrt(camera_ray[0]**2 + camera_ray[1]**2 + camera_ray[2]**2)
        camera_ray /= distance
        
        if np.dot(normal, camera_ray) < 0:
            z_order[i] = -distance
        else:
            z_order[i] = 9999


@njit()
def project_points(vertices, camera, theta=1e-16):
    output = np.empty((len(vertices), 2)) # Change to use persistent list for speed?
    
    for i, v in enumerate(vertices):
        
        # Vertical x, y angle between camera and point
        h_angle_camera_point = np.arctan((v[2]-camera[2]) / (v[0]-camera[0] + theta))

        # If the point is behind the camera, flip the angle        
        if abs(camera[0] + np.cos(h_angle_camera_point) - v[0]) > abs(camera[0] - v[0]):
            h_angle_camera_point = (h_angle_camera_point - np.pi) % (2 * np.pi)
        
        # Difference between camera angle and point angle
        h_angle = (h_angle_camera_point - camera[3]) % (2 * np.pi)
        
        # Bring angle into range [-pi, pi]
        if h_angle > np.pi:
            h_angle -= 2 * np.pi
        
        # Calculate the horizontal screen coordinate
        x = SCREEN_W * h_angle / FOV_H + SCREEN_W / 2
        
        # Calculate xy distance from camera to point
        distance = np.sqrt((v[0]-camera[0])**2 + (v[1]-camera[1])**2 + (v[2]-camera[2])**2)
        
        # Calculate angle to xy plane
        v_angle_camera_point = np.arcsin((camera[1]-v[1])/distance) # np.arctan((v[1]-camera[1]) / (v[0]-camera[0] + theta))
        
        # Calculate difference between camera vertical angle and point vertical angle
        v_angle = (v_angle_camera_point - camera[4]) % (2 * np.pi)
        
        # Bring angle into range [-pi, pi]
        if v_angle > np.pi:
            v_angle -= 2 * np.pi
        
        y = SCREEN_H * v_angle / FOV_V + SCREEN_H / 2
        
        output[i] = (x, y)
        
    return output
        
if __name__ == '__main__':
    main()