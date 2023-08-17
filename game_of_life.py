import numpy as np


class GameOfLife():
    def __init__(self, width=10, height=10, radius=1, rules=None, initial_state=None, randomize_percent=0.5):
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
        
        self.radius = radius
        
        self.rules = rules if rules is not None else {True: {2: True, 3: True}, False: {3: True}}
    
    def get_neighbors(self, i: int, j: int, radius=1):
        # num_neighbors = 0
        num_neighbors = np.sum(self.state[max(0, i - radius):i + radius + 1, max(0, j - radius):j + radius + 1]) - self.state[i, j]
        #  X . .
        #  . . .
        #  . X X

        # for k in range(-radius, 1 + radius):
        #     for l in range(-radius, 1 + radius):
        #         if k == 0 and l == 0:
        #             continue
        #         elif i + k < 0 or i + k >= self.height:
        #             continue
        #         elif j + l < 0 or j + l >= self.width:
        #             continue
        #         elif self.state[i + k, j + l]:
        #             num_neighbors += 1
                    
        return num_neighbors
    
    def step(self):
        new_state = np.zeros((self.height, self.width), dtype=np.bool_)
        for i in range(self.height):
            for j in range(self.width):
                new_state[i, j] = self.rules[self.state[i,j]].get(self.get_neighbors(i, j, self.radius), False)
        self.state = new_state
    
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