# Nathaniel Youngren
# Using: https://youtu.be/D96wb46mjIQ as a guide

import pygame as pg
import numpy as np
from numba import njit
from geometry import Geometry_3D


SCREEN_W, SCREEN_H = 800, 600
FOV_V = np.pi / 5
FOV_H = FOV_V * SCREEN_W / SCREEN_H



def main():
    
    # Read file
    obj_file = 'assets/teapot.obj'
    geometry = Geometry_3D()
    geometry.read(obj_file)

    pg.init()
    pg.display.set_caption('Renderer Test')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()


    surf = pg.surface.Surface((SCREEN_W, SCREEN_H))    

    pixel_coords = np.empty((len(geometry.vertices), 2))
    
    z_order = np.empty(len(geometry.faces))
    shade = np.empty(len(geometry.faces))
    
    camera = np.array([13, 0.5, 2, 3.3, 0])
    
    
    while running:


        elapsed_time = clock.tick(60) * 0.001
        surf.fill((50, 127, 200)) 
        
        # Define rotating light source
        light_dir = np.array([np.sin(pg.time.get_ticks()/1000), 1, 1])
        light_dir = light_dir/np.linalg.norm(light_dir)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    print('space pressed')
        
        project_points(geometry.vertices, camera, pixel_coords)
        sort_faces(geometry.vertices, geometry.faces, camera, z_order, light_dir, shade)

        for i in np.argsort(z_order):
            
            if z_order[i] == np.inf:
                break
            
            v_is = geometry.faces[i]
            triangle = [pixel_coords[index] for index in v_is]
            color = abs(shade[i]) * np.abs(geometry.vertices[v_is[0]]) * 45 + 25
            pg.draw.polygon(surf, color, triangle)
        
        screen.blit(surf, (0, 0))
        
        pg.display.flip()
        pg.display.set_caption(str(round(1/(elapsed_time+1e-16), 2)) + ' fps : ' + str(camera) )
        
        move_camera(camera, elapsed_time)


def move_camera(camera, elapsed_time):
    
    if pg.mouse.get_focused():
        p_mouse = pg.mouse.get_rel()
        if pg.mouse.get_pos() != (SCREEN_W/2, SCREEN_H/2):
            pg.mouse.set_pos((SCREEN_W/2, SCREEN_H/2))
        camera[3] = (camera[3] + 10 * elapsed_time * np.clip((p_mouse[0])/SCREEN_W, -0.2, 0.2)) % (2*np.pi)
        camera[4] = camera[4] + 10 * elapsed_time * np.clip((p_mouse[1])/SCREEN_H, -0.2, 0.2)
        camera[4] = np.clip(camera[4], -0.3, 0.3) #-np.pi/2, np.pi/2)

    pressed_keys = pg.key.get_pressed()
    
    if pressed_keys[pg.K_w] or pressed_keys[pg.K_s] and pressed_keys[pg.K_a] or pressed_keys[pg.K_d]:
        elapsed_time /= np.sqrt(2)
    
    
    if pressed_keys[pg.K_w]:
        camera[0] += 10 * elapsed_time * np.cos(camera[3])
        camera[2] += 10 * elapsed_time * np.sin(camera[3])
    elif pressed_keys[pg.K_s]:
        camera[0] -= 10 * elapsed_time * np.cos(camera[3])
        camera[2] -= 10 * elapsed_time * np.sin(camera[3])
    
    if pressed_keys[pg.K_a]:
        camera[0] += 10 * elapsed_time * np.sin(camera[3])
        camera[2] -= 10 * elapsed_time * np.cos(camera[3])
    elif pressed_keys[pg.K_d]:
        camera[0] -= 10 * elapsed_time * np.sin(camera[3])
        camera[2] += 10 * elapsed_time * np.cos(camera[3])
            
    
@njit()
def sort_faces(vertices, faces, camera, z_order, light_dir, shade):
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
        
        if dot_3d(normal, camera_ray) < 0:
            z_order[i] = -distance
            shade[i] = dot_3d(light_dir, normal)/2 + 0.5
        else:
            z_order[i] = np.inf
            
@njit()
def dot_3d(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

@njit()
def project_points(vertices, camera, pixel_coords, theta=1e-16):
    
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
        
        pixel_coords[i] = (x, y)
                
if __name__ == '__main__':
    main()
