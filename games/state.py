class Action:
    def __init__(self, idx) -> None:
        self.idx = idx

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'action({self.idx})'
    
class State:
    def __init__(self):
        self.terminal_status = (False, None)

    def apply_action(self, action):
        next_st = self.copy()
        next_st.update_state(action)
        next_st.terminal_status = next_st.check_terminal()
        # if not next_st.terminal_status[0]:
        next_st.change_player()
        return next_st
    
    def get_value(self):
        assert(self.is_terminal())
        return self.terminal_status[1]

    def is_terminal(self):
        return self.terminal_status[0]

    def change_player(self):
        pass

    def update_state(self, action):
        pass

    def copy(self):
        pass

    def is_max_player(self):
        pass
        
    def available_actions(self):
        pass

    def check_terminal(self):
        pass

    def get_next_player(self):
        pass
