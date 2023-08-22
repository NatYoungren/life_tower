# Nathaniel Youngren
# Using: https://youtu.be/D96wb46mjIQ as a guide

import pygame as pg
import numpy as np
from game_of_life import GameOfLife
from geometry import Geometry_3D

import renderer
from renderer import move_camera, sort_faces, project_points
from geometry import generate_diamond


# SCREEN SETTINGS
SQUARE_CELLS = True
SCREEN_W, SCREEN_H = 1200, 800
CELL_COLOR = (180, 240, 50)
AGED_COLOR = (80, 75, 60)
BG_COLOR = (78,75,55)
BOARD_COLOR = [78,75,55]
OFFSET_X, OFFSET_Y = 0, 0
CENTER_OFFSET = (-0.05, -0.05)

# SIMULATION SETTINGS
MANUAL_CONTROL = False
BOARD_W, BOARD_H = 10, 10
STORED_STATES = 40
TICK_MAX = 1

# # CELL CALCULATIONS
CELL_SCALE = 1
GRID_SIZE = 1
# CELL_W = SCREEN_W / BOARD_W
# CELL_H = SCREEN_H / BOARD_H
# if SQUARE_CELLS: CELL_W = CELL_H = min(CELL_W, CELL_H)
# ORIGIN_X = (SCREEN_W - CELL_W * BOARD_W) / 2
# ORIGIN_Y = (SCREEN_H - CELL_H * BOARD_H) / 2
# CENTER = (ORIGIN_X + CELL_W * BOARD_W / 2, ORIGIN_Y + CELL_H * BOARD_H / 2)
STATE_STORE = np.zeros((STORED_STATES, BOARD_H, BOARD_W), dtype=np.bool_)
COLOR_INTERP = np.array([np.linspace(c1, c2, STORED_STATES, dtype=np.int_) for c1, c2 in zip(CELL_COLOR, AGED_COLOR)]).T



# TODO: Add function to renderer for setting up these variables
# NOTE: Consider using a class for this
renderer.SCREEN_W, renderer.SCREEN_H = 800, 600
renderer.FOV_V = np.pi / 5
renderer.FOV_H = renderer.FOV_V * renderer.SCREEN_W / renderer.SCREEN_H


def main():
    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3, radius=1, rules={True: {2: True, 3: True}, False: {3: True}})
    print(game)
    obj = Geometry_3D()
    # obj.vertices, obj.faces = generate_diamond()

    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((renderer.SCREEN_W, renderer.SCREEN_H))
    running = True
    clock = pg.time.Clock()

    surf = pg.surface.Surface((renderer.SCREEN_W, renderer.SCREEN_H))    

    # NOTE: Consider storing these in geometry class or renderer module
    

    
    camera = np.array([13, 4, 2, 3.3, 0])
    # light_dir = np.array([0, 1, 1])
    for i in range(game.height):
            for j in range(game.width):
                if game.state[i, j]:
                    v, f = generate_diamond(offset=(i*GRID_SIZE, 0, -j*GRID_SIZE), scale=CELL_SCALE)
                    f += int(len(obj.vertices)/3)
                    # print(obj.vertices/3,v)
                    obj.vertices = np.append(obj.vertices, v)
                    obj.faces = np.append(obj.faces, f)

    obj.vertices = obj.vertices.reshape(-1,3)
    obj.faces = obj.faces.reshape(-1,3)
    
    # Used to store projected points
    pixel_coords = np.empty((len(obj.vertices), 2))
    
    # Used to order faces by depth
    z_order = np.empty(len(obj.faces))
    
    # Used to store shading values, derived from angle between face normal and light direction
    shade = np.empty(len(obj.faces))
    
    
    while running:
        elapsed_time = clock.tick(60) * 0.001
        surf.fill((50, 127, 200)) 
        
        # Define rotating light source
        light_dir = np.array([np.sin(pg.time.get_ticks()/1000)-1, 1, 1])
        light_dir = light_dir/np.linalg.norm(light_dir)
        
        
        
        # obj.vertices, obj.faces = generate_diamond(offset=(np.sin(pg.time.get_ticks()/1000), 0, 0))

        # light_dir = camera[:3]/np.linalg.norm(camera[:3])
        # print('events')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    game.step()
                    print(game)
                    obj.vertices -= (0, 1, 0)
                    for i in range(game.height):
                        for j in range(game.width):
                            if game.state[i, j]:
                                v, f = generate_diamond(offset=(i*GRID_SIZE, 0, -j*GRID_SIZE), scale=CELL_SCALE)
                                f += len(obj.vertices)
                                # print(obj.vertices/3,v)
                                obj.vertices = np.append(obj.vertices, v)
                                obj.faces = np.append(obj.faces, f)

                                obj.vertices = obj.vertices.reshape(-1,3)
                                obj.faces = obj.faces.reshape(-1,3)
                    
                    # Used to store projected points
                    pixel_coords = np.empty((len(obj.vertices), 2))
                    
                    # Used to order faces by depth
                    z_order = np.empty(len(obj.faces))
                    
                    # Used to store shading values, derived from angle between face normal and light direction
                    shade = np.empty(len(obj.faces))
        
        project_points(obj.vertices, camera, pixel_coords)
        sort_faces(obj.vertices, obj.faces, camera, z_order, light_dir, shade)

        for i in np.argsort(z_order):
            
            if z_order[i] == np.inf: # TODO: Improve this to avoid repetitive if statement?
                break
            
            v_is = obj.faces[i]
            triangle = [pixel_coords[index] for index in v_is]
            color = shade[i] * COLOR_INTERP[0]
            pg.draw.polygon(surf, color, triangle)
        
        screen.blit(surf, (0, 0))
        
        # print('flipping')
        pg.display.flip()
        pg.display.set_caption(str(round(1/(elapsed_time+1e-16), 2)) + ' fps : ' + str(camera) )

        move_camera(camera, elapsed_time)

if __name__ == '__main__':
    main()
