import pygame as pg
import numpy as np
from game_of_life import GameOfLife
import debug_timer

# SCREEN SETTINGS
SQUARE_CELLS = True
SCREEN_W, SCREEN_H = 1920, 1080
CELL_COLOR = (180, 240, 50)
AGED_COLOR = (70, 50, 50)
BG_COLOR = (190, 210, 240)
BOARD_COLOR = [min(255, int(c*2)) for c in BG_COLOR]
OFFSET_X, OFFSET_Y = 0, 0
CENTER_OFFSET = (-0.05, -0.05)

# SIMULATION SETTINGS
MANUAL_CONTROL = False
BOARD_W, BOARD_H = 160, 90
STORED_STATES = 10
TICK_MAX = 15

# CELL CALCULATIONS
CELL_W = SCREEN_W / BOARD_W
CELL_H = SCREEN_H / BOARD_H
if SQUARE_CELLS: CELL_W = CELL_H = min(CELL_W, CELL_H)
ORIGIN_X = (SCREEN_W - CELL_W * BOARD_W) / 2
ORIGIN_Y = (SCREEN_H - CELL_H * BOARD_H) / 2
CENTER = (ORIGIN_X + CELL_W * BOARD_W / 2, ORIGIN_Y + CELL_H * BOARD_H / 2)
STATE_STORE = np.zeros((STORED_STATES, BOARD_H, BOARD_W), dtype=np.bool_)
COLOR_INTERP = np.array([np.linspace(c1, c2, STORED_STATES, dtype=np.int_) for c1, c2 in zip(CELL_COLOR, AGED_COLOR)]).T


# Store the current state in the state store and shift the rest down
def store_state(state):
    if not STORED_STATES: return
    global STATE_STORE
    STATE_STORE = np.roll(STATE_STORE, 1, axis=0)
    STATE_STORE[0] = state

# Reset all states to zeros
def reset_states():
    if not STORED_STATES: return
    global STATE_STORE
    STATE_STORE = np.zeros((STORED_STATES, BOARD_H, BOARD_W), dtype=np.bool_)

def main():
    timer = debug_timer.DebugTimer()

    pg.init()
    pg.display.set_caption('Tower of Life')
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    
    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3, radius=1, rules={True: {2: True, 3: True}, False: {3: True}})
    tick_count = 0
    
    # Draw a state on the screen with a given color and offset
    def draw_state(surface, state, color, offset=(0, 0), center_offset=(0, 0)):
        for i in range(BOARD_H):
            for j in range(BOARD_W):
                if state[i, j]:
                    
                    # Calculate the position of the cell (top left corner)
                    x, y = ORIGIN_X + CELL_W * j, ORIGIN_Y + CELL_H * i
                    
                    # Calculate the offset, (optionally based on a vector from the center of the board to the center of the cell)
                    if any(center_offset):
                        x_diff, y_diff = (x + CELL_W/2) - CENTER[0], (y + CELL_H/2) - CENTER[1]                        
                        x_diff, y_diff =  offset[0] + (x_diff * center_offset[0] / BOARD_W*CELL_W),  offset[1] + (y_diff * center_offset[1] / BOARD_H*CELL_H)
                    else:
                        x_diff, y_diff = offset[0], offset[1]
                        
                    # Draw the cell
                    pg.draw.rect(surface, color, (x + x_diff, y + y_diff, CELL_W, CELL_H), 0)
    
    # Update the screen with all the stored states
    def update_screen():
        # Fill board color
        screen.fill(BOARD_COLOR)

        # Draw stored states
        for i in range(STORED_STATES-1, -1, -1):
            offset = (OFFSET_X * i, OFFSET_Y * i)
            center_offset = (CENTER_OFFSET[0] * i, CENTER_OFFSET[1] * i)
            draw_state(screen, STATE_STORE[i], COLOR_INTERP[i], offset, center_offset)
            
        # Draw borders
        pg.draw.rect(screen, BG_COLOR, (0, 0, ORIGIN_X, SCREEN_H), 0)
        pg.draw.rect(screen, BG_COLOR, (0, 0, SCREEN_W, ORIGIN_Y), 0)
        pg.draw.rect(screen, BG_COLOR, (SCREEN_W - ORIGIN_X, 0, ORIGIN_X, SCREEN_H), 0)
        pg.draw.rect(screen, BG_COLOR, (0, SCREEN_H - ORIGIN_Y, SCREEN_W, ORIGIN_Y), 0)
        
        # Render current state
        pg.display.flip()

    # Main loop
    while running:

        tick_count += 1
        # Handle input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            # Handle keypresses
            elif event.type == pg.KEYDOWN:
                
                # Escape key quits
                if event.key == pg.K_ESCAPE:
                    running = False
                    
                # Spacebar steps the simulation if manual control is enabled
                elif event.key == pg.K_SPACE and MANUAL_CONTROL:
                    game.step()
                    store_state(game.state) 
                    update_screen()
                    
                # R key resets the simulation
                elif event.key == pg.K_r:
                    game = GameOfLife(width=BOARD_W, height=BOARD_H, randomize_percent=0.3)
                    reset_states()
        timer.lap('loop')

        # Step the simulation automatically if manual control is disabled
        if not MANUAL_CONTROL and tick_count >= TICK_MAX:
            game.step()
            timer.lap('step')
            store_state(game.state)
            timer.lap('store')
            update_screen()
            tick_count = 0
            timer.lap('update')
            
    timer.print_laps()
            
if __name__ == '__main__':
    main()