from games.state import *
import numpy as np
from scipy.signal import convolve2d

class Connect4State(State):
    height = 6
    width = 7
    blank = 0

    def __init__(self) -> None:
        super().__init__()
        self.values = np.zeros((Connect4State.height, Connect4State.width), dtype=np.int8)
        self.player = 1

    def available_actions(self):
        return [Action(i) for i, x in enumerate(self.values[0]) if x == Connect4State.blank]
    
    def change_player(self):
       self.player *= -1

    def copy(self):
        st = Connect4State()
        st.values = self.values.copy()
        st.player = self.player
        return st

    def update_state(self, action):
        for i in reversed(range(Connect4State.height)):
            if self.values[i][action.idx] == Connect4State.blank:
                self.values[i][action.idx] = self.player
                break
    
    def is_max_player(self):
        return self.player == 1

    def get_value_player_agnostic(self):
        return self.get_value() * self.player

    def check_terminal(self):
        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        all_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

        for kernel in all_kernels:
            if (convolve2d(self.values == 1, kernel, mode="valid") == 4).any():
                return True, 1
            if (convolve2d(self.values == -1, kernel, mode="valid") == 4).any():
                return True, -1

        if not np.any(self.values == Connect4State.blank):
            return True, 0
        return False, None

    def get_next_player(self):
        return self.player

    @staticmethod
    def get_symbol(player):
        if player == 1:
            return 'A'
        elif player == -1:
            return 'B'
        else:
            return ' '

    def get_next_player_ext(self):
        return Connect4State.get_symbol(self.player)

    def __str__(self) -> str:
        s = ''
        for i in range(self.values.shape[0]):
            for j in range(self.values.shape[1]):
                s += f'{Connect4State.get_symbol(self.values[i][j])}  '
            s += '\n'
        s += '-  -  -  -  -  -  -\n'
        s += '0  1  2  3  4  5  6\n'
        return f'{s}' + f'\n next player: {self.get_next_player_ext()} ' + f'terminal status: {self.terminal_status}'

# st = Connect4State()
# print(st.values)
# st = st.apply_action(st.available_actions()[0])
# st = st.apply_action(st.available_actions()[1])
# st = st.apply_action(st.available_actions()[0])
# st = st.apply_action(st.available_actions()[1])
# st = st.apply_action(st.available_actions()[0])
# st = st.apply_action(st.available_actions()[1])
# print(st.check_terminal())
# st = st.apply_action(st.available_actions()[0])
# print(st)
# print(st.check_terminal())
# print(st.available_actions())