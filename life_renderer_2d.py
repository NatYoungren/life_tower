import pygame as pg
import numpy as np
from game_of_life import GameOfLife

# SCREEN SETTINGS
SQUARE_CELLS = True
SCREEN_W, SCREEN_H = 1920, 1080
CELL_COLOR = (250, 180, 250)
AGED_COLOR = (100, 50, 100)
BG_COLOR = (25, 50, 25)
BOARD_COLOR = [min(255, int(c*2)) for c in BG_COLOR]

# SIMULATION SETTINGS
MANUAL_CONTROL = False
BOARD_W, BOARD_H = 160, 90
STORED_STATES = 10

# CELL CALCULATIONS
CELL_W = SCREEN_W / BOARD_W
CELL_H = SCREEN_H / BOARD_H
if SQUARE_CELLS: CELL_W = CELL_H = min(CELL_W, CELL_H)
ORIGIN_X = (SCREEN_W - CELL_W * BOARD_W) / 2
ORIGIN_Y = (SCREEN_H - CELL_H * BOARD_H) / 2
STATE_STORE = np.zeros((STORED_STATES, BOARD_H, BOARD_W), dtype=np.bool_)
COLOR_INTERP = np.array([np.linspace(c1, c2, STORED_STATES, dtype=np.int_) for c1, c2 in zip(CELL_COLOR, AGED_COLOR)]).T

def main():
    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()
    
    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3)
    tick_max = 15
    tick_count = 0
    
    def store_state(state):
        if not STORED_STATES: return
        global STATE_STORE
        STATE_STORE = np.roll(STATE_STORE, 1, axis=0)
        STATE_STORE[0] = state
    
    def draw_state(surface, state, color, offset=(0, 0)):
        for i in range(BOARD_H):
            for j in range(BOARD_W):
                if state[i, j]:
                    pg.draw.rect(surface, color, (ORIGIN_X + CELL_W * j + offset[0], ORIGIN_Y + CELL_H * i + offset[1], CELL_W, CELL_H), 0)

    def update_screen():
        # Fill board color
        screen.fill(BOARD_COLOR)
        # Draw stored states
        for i in range(STORED_STATES-1, -1, -1):
            draw_state(screen, STATE_STORE[i], COLOR_INTERP[i])
            
        # Draw borders
        pg.draw.rect(screen, BG_COLOR, (0, 0, ORIGIN_X, SCREEN_H), 0)
        pg.draw.rect(screen, BG_COLOR, (0, 0, SCREEN_W, ORIGIN_Y), 0)
        pg.draw.rect(screen, BG_COLOR, (SCREEN_W - ORIGIN_X, 0, ORIGIN_X, SCREEN_H), 0)
        pg.draw.rect(screen, BG_COLOR, (0, SCREEN_H - ORIGIN_Y, SCREEN_W, ORIGIN_Y), 0)
        
        # Draw current state
        pg.display.flip()

    
    while running:
        tick_count += 1

        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE and MANUAL_CONTROL:
                    game.step()
                    store_state(game.state)
                    update_screen()
                elif event.key == pg.K_r:
                    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3)
                    
        if not MANUAL_CONTROL and tick_count >= tick_max:
            game.step()
            store_state(game.state)
            update_screen()
            tick_count = 0
            
        clock.tick()
if __name__ == '__main__':
    main()