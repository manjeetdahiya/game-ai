from games.state import *

class Game:
    def __init__(self, intial_state) -> None:
        self.history_states = [intial_state]

    def play(self, action):
        st = self.get_last_state().apply_action(action)
        self.history_states.append(st)

    def get_last_state(self):
        return self.history_states[-1]