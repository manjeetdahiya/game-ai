from games.state import *
import numpy as np
from scipy.signal import convolve2d

class TTTAction(Action):
    def get_x(self):
        return self.idx // 3

    def get_y(self):
        return self.idx % 3

    def __str__(self) -> str:
        return f'Action({self.get_x()}, {self.get_y()})'

class TTTState(State):
    blank = 0

    def __init__(self) -> None:
        super().__init__()
        self.values = np.zeros((3, 3), dtype=np.int8)
        self.player = 1

    def __str__(self) -> str:
        return f'{self.values}' + f'\n player: {self.player}'

    def get_value_player_agnostic(self):
        return self.get_value() * self.player

    def is_max_player(self):
        return self.player == 1
        
    def available_actions(self):
        return [TTTAction(i*3+j)  for i in range(3) 
                                    for j in range(3) 
                                        if self.values[i][j] == TTTState.blank]
    
    def change_player(self):
        self.player *= -1
    
    def copy(self):
        st = TTTState()
        st.values = self.values.copy()
        st.player = self.player
        return st

    def update_state(self, action):
        self.values[action.get_x()][action.get_y()] = self.player
    
    def check_terminal(self):
        horizontal_kernel = np.array([[1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(3, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        all_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

        for kernel in all_kernels:
            if (convolve2d(self.values == 1, kernel, mode="valid") == 3).any():
                return True, 1
            if (convolve2d(self.values == -1, kernel, mode="valid") == 3).any():
                return True, -1

        if not np.any(self.values == TTTState.blank):
            return True, 0
        return False, None
