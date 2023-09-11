from games.game import *
from games.tic_tac_toe import *
from games.connect4 import *

from algorithms.MiniMax import *
from algorithms.MCTS import *

import operator
import random

gm = Game(Connect4State())
assert(gm.get_last_state().is_max_player())

while True:
    print(gm.get_last_state())
    if gm.get_last_state().is_terminal():
        print(gm.get_last_state().terminal_status, gm.get_last_state().player)
        break
    if gm.get_last_state().is_max_player():
        actions_dict = {i: a for i, a in enumerate(gm.get_last_state().available_actions())}
        a_input = input(f'take action: {actions_dict}\n=')
        a = actions_dict[int(a_input)]
        print(f'Action taken by {gm.get_last_state().player}: {a.idx}')
    else:
        mcts = MCTS()
        action_probs = mcts.search(gm.get_last_state(), 10_000)
        # print(action_probs)
        a, r = max(action_probs, key=operator.itemgetter(1))
        print(f'Action decided by {gm.get_last_state().player}: ||{a.idx}|| for reward {r}')
    gm.play(a)


