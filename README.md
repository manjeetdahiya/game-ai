# game-ai

Small playground for game-playing AI algorithms, with Tic-Tac-Toe and Connect 4 as test games.

## Algorithms

- **Minimax** ([algorithms/MiniMax.py](algorithms/MiniMax.py)): exhaustive search (no alpha-beta pruning yet), suited to Tic-Tac-Toe.
- **MCTS** ([algorithms/MCTS.py](algorithms/MCTS.py)): Monte Carlo Tree Search with UCB selection.

## Games

- Tic-Tac-Toe ([games/tic_tac_toe.py](games/tic_tac_toe.py))
- Connect 4 ([games/connect4.py](games/connect4.py))

New games subclass `State` in [games/state.py](games/state.py).

## Usage

Requires Python 3 with `numpy` and `scipy`:

```sh
pip install numpy scipy
python main.py
```

`main.py` starts a Connect 4 game where you play as the first (max) player by entering an action index, and the MCTS agent (10,000 simulations per move) plays the second. Edit `main.py` to change the game or algorithm.

## License

[MIT](LICENSE)
