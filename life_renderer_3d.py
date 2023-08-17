import pygame as pg
import numpy as np
from game_of_life import GameOfLife

SCREEN_W, SCREEN_H = 800, 600
FOV_V = np.pi / 5
FOV_H = FOV_V * SCREEN_W / SCREEN_H

MANUAL_CONTROL = False
SQUARE_CELLS = True
BOARD_W, BOARD_H = 100, 100

CELL_W = SCREEN_W / BOARD_W
CELL_H = SCREEN_H / BOARD_H
if SQUARE_CELLS: CELL_W = CELL_H = min(CELL_W, CELL_H)
ORIGIN_X = (SCREEN_W - CELL_W * BOARD_W) / 2
ORIGIN_Y = (SCREEN_H - CELL_H * BOARD_H) / 2
# print(CELL_W, CELL_H, ORIGIN_X, ORIGIN_Y)

def main():
    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()
    # surf = pg.surface.Surface((SCREEN_W, SCREEN_H))
    
    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3)
    state = game.state
    tick_max = 15
    tick_count = 0
    
    while running:
        screen.fill((20, 40, 20))

        tick_count += 1

        # Draw borders
        pg.draw.rect(screen, (50, 100, 50), (ORIGIN_X, ORIGIN_Y, CELL_W * BOARD_W, CELL_H * BOARD_H), 0)
        
        for i in range(BOARD_H):
            for j in range(BOARD_W):
                if state[i, j]:
                    pg.draw.rect(screen, (255, 200, 255), (ORIGIN_X + CELL_W * j, ORIGIN_Y + CELL_H * i, CELL_W, CELL_H), 0)
        pg.display.flip()
        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE and MANUAL_CONTROL:
                    game.step()
                    state = game.state
                elif event.key == pg.K_r:
                    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3)
                    state = game.state
                    
        if not MANUAL_CONTROL and tick_count >= tick_max:
            game.step()
            state = game.state
            tick_count = 0
            
        clock.tick()
if __name__ == '__main__':
    main()