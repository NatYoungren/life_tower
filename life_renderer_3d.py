# Nathaniel Youngren
# Using: https://youtu.be/D96wb46mjIQ as a guide

import pygame as pg
import numpy as np
from numba import njit
from geometry import Geometry_3D
import renderer
from renderer import move_camera, sort_faces, project_points
from geometry import generate_diamond


SCREEN_W, SCREEN_H = 800, 600
FOV_V = np.pi / 5
FOV_H = FOV_V * SCREEN_W / SCREEN_H

obj_file = 'assets/teapot.obj'
obj = Geometry_3D(obj_file)
# obj_reader.vertices = np.asarray([[1, 1, 1], [4, 2, 0], [1, 0.5, 3]])
# obj_reader.faces = np.asarray([[0, 1, 2]])

obj.vertices, obj.faces = generate_diamond()
# print(np.mean(obj_reader.vertices, axis=0))


def main():
    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()


    surf = pg.surface.Surface((SCREEN_W, SCREEN_H))    

    pixel_coords = np.empty((len(obj.vertices), 2))
    
    z_order = np.empty(len(obj.faces))
    shade = np.empty(len(obj.faces))
    
    camera = np.array([13, 0.5, 2, 3.3, 0])
    # light_dir = np.array([0, 1, 1])
    
    
    while running:
        # print('start_pos', pg.mouse.get_pos())
        # pg.mouse.set_pos((SCREEN_W/2, SCREEN_H/2))

        elapsed_time = clock.tick(60) * 0.001
        surf.fill((50, 127, 200)) 
        
        # Define rotating light source
        light_dir = np.array([np.sin(pg.time.get_ticks()/1000)-1, 1, 1])
        light_dir = light_dir/np.linalg.norm(light_dir)
        obj.vertices, obj.faces = generate_diamond(offset=(np.sin(pg.time.get_ticks()/1000), 0, 0))

        # light_dir = camera[:3]/np.linalg.norm(camera[:3])
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    print('space pressed')
        
        project_points(obj.vertices, camera, pixel_coords)
        sort_faces(obj.vertices, obj.faces, camera, z_order, light_dir, shade)

        for i in np.argsort(z_order):
            
            if z_order[i] == np.inf:
                break
            
            v_is = obj.faces[i]
            triangle = [pixel_coords[index] for index in v_is]
            color = abs(shade[i]) * np.abs(obj.vertices[v_is[0]]) * 45 + 25
            pg.draw.polygon(surf, color, triangle)
        
        screen.blit(surf, (0, 0))
        
        pg.display.flip()
        pg.display.set_caption(str(round(1/(elapsed_time+1e-16), 2)) + ' fps : ' + str(camera) )
        
        move_camera(camera, elapsed_time)
                
if __name__ == '__main__':
    main()
