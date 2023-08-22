import numpy as np
from numba import njit

@njit()
def fast_step(nmap, state, h, w):
    nmap *= 0
    for i in range(h):
        for j in range(w):
            if state[i, j]:
                nmap[max(0, i - 1):i + 1 + 1, max(0, j - 1):j + 1 + 1] += 1
                
    for i in range(h):
        for j in range(w):
            # if state[i, j]:
            #     state[i, j] = nmap[i, j] in [3, 4] # These numbers are increased by 1, as [i, j] is counted as a living neighbor
            # else:
            #     state[i, j] = nmap[i, j] in 3
            state[i, j] = nmap[i, j] == 3 or state[i, j] and nmap[i, j] == 4


class GameOfLife():
    # TODO: Deprecate radius and rules
    def __init__(self, width=10, height=10, radius=1, rules=None, initial_state=None, randomize_percent=0.3):
        self.width = width
        self.height = height
        
        if initial_state is None:
            self.state = np.zeros((height, width), dtype=np.bool_)
            
            for i in range(height):
                for j in range(width):
                    if np.random.random() < randomize_percent:
                        self.state[i, j] = True
        else:
            self.state = initial_state
        
        self.neighbor_map = np.zeros((height, width), dtype=int)
        
        # NOTE: Not used by fast_step
        self.radius = radius
        self.rules = rules if rules is not None else {True: {2: True, 3: True}, False: {3: True}}
    
    def faster_but_uglier_get_neighbors(self, i: int, j: int, radius=1):
        num_neighbors = 0
        for k in range(-radius, 1 + radius):
            for l in range(-radius, 1 + radius):
                if k == 0 and l == 0:
                    continue
                elif i + k < 0 or i + k >= self.height:
                    continue
                elif j + l < 0 or j + l >= self.width:
                    continue
                elif self.state[i + k, j + l]:
                    num_neighbors += 1
        return num_neighbors

    def get_neighbors(self, i: int, j: int, radius=1):
        return np.sum(self.state[max(0, i - radius):i + radius + 1, max(0, j - radius):j + radius + 1]) - self.state[i, j]
    
    def slow_step(self):
        new_state = np.zeros((self.height, self.width), dtype=np.bool_)
        for i in range(self.height):
            for j in range(self.width):
                new_state[i, j] = self.rules[self.state[i,j]].get(self.get_neighbors(i, j, self.radius), False)
        self.state = new_state
    
    def gen_neighbor_map(self):
        neighbor_map = np.zeros((self.height, self.width), dtype=np.uint8)

        for i in range(self.height):
            for j in range(self.width):
                if self.state[i, j]:
                    neighbor_map[max(0, i - self.radius):i + self.radius + 1, max(0, j - self.radius):j + self.radius + 1] += 1
        return neighbor_map
    
    def slow_step2(self):
        nm = self.gen_neighbor_map()
        for i in range(self.height):
            for j in range(self.width):
                self.state[i, j] = self.rules[self.state[i, j]].get(nm[i, j] - self.state[i, j], False)

    def step(self):
        fast_step(self.neighbor_map, self.state, self.height, self.width)
    
    def __repr__(self):
        board = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.state[i, j]:
                    board += 'X '
                else:
                    board += '. '
            board += '\n'
        return board
    
if __name__ == '__main__':
    game = GameOfLife()
    for i in range(10):
        print(game)
        game.step()
