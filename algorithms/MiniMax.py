from games.state import *
from games.game import *
import games.tic_tac_toe as ttt
import operator

# TODO: alpha-beta pruning
def minimax(s) -> (Action, int):
    is_terminal, reward = s.terminal_status
    if is_terminal:
        return None, reward

    assert(len(s.available_actions()) > 0)
 
    all_next_rewards = [(a, minimax(s.apply_action(a))[1]) for a in s.available_actions()]
    if s.is_max_player():
        return max(all_next_rewards, key=operator.itemgetter(1))
    else:
        return min(all_next_rewards, key=operator.itemgetter(1))


# tests
