from games.state import *
from games.game import *
import math
import operator
import random

class Node:
    def __init__(self, state: State, parent, children, action) -> None:
        self.parent = parent
        self.children = children
        self.state = state
        self.action = action

        self.value_sum = 0
        self.visit_count = 0

    def add_child(self, child):
        self.children.append(child)

    def is_exapansion_possible(self):
        return len(self.unseen_actions()) > 0
    
    def calculate_ucb(self):
        C = 1.4
        Np = self.parent.visit_count
        N = self.visit_count
        v_avg = self.value_sum/N
        q_value = v_avg
        return q_value + C * math.sqrt(math.log(Np) / N)
    
    def unseen_actions(self):
        actions_taken = set([child.action.idx for child in self.children])
        unseen_actions = [a for a in self.state.available_actions() if a.idx not in actions_taken]
        return unseen_actions
    
    def __str__(self) -> str:
        s = f'\nNode: {id(self)}'
        s += f'\nvalue_sum: {self.value_sum}\n'
        s += f'visti_count: {self.visit_count}\n'
        s += '\nChildren:\n'
        s += str([id(child) for child in self.children])
        return s
    
    @staticmethod
    def print_graph(n):
        s = str(n)
        for child in n.children:
            s += Node.print_graph(child)
        return s

class MCTS:
    def __init__(self) -> None:
        pass

    @staticmethod
    def select(n) -> Node:
        while len(n.children) > 0 and not n.is_exapansion_possible():
            child_ucbs = [(child, child.calculate_ucb()) for child in n.children]
            child, _ = max(child_ucbs, key=operator.itemgetter(1))
            n = child
        return n
    
    @staticmethod
    def expand(n: Node) -> Node:
        action = random.choice(n.unseen_actions())
        child = Node(n.state.apply_action(action), parent=n, children=[], action=action)
        n.add_child(child)

        # action = random.choice(child.unseen_actions())
        # child2 = Node(n.state.apply_action(action), parent=child, children=[], action=action)
        # child.add_child(child2)

        return child

    @staticmethod
    def simulate(n: Node) -> int:
        gm = Game(n.state)

        while not gm.get_last_state().is_terminal():
            action = random.choice(gm.get_last_state().available_actions())
            gm.play(action)

        return gm.get_last_state().get_value()

    @staticmethod
    def backpropagate(n: Node, value):
        while n:
            # player denotes next player
            # value is switched on player change
            n.value_sum += value * n.state.player * -1
            n.visit_count += 1
            n = n.parent

    def search(self, root_state: State, search_quota):
        root = Node(root_state, None, [], action=None)
        
        for _ in range(search_quota):
            # print([(child.action, child.calculate_ucb()) for child in root.children])
            n = MCTS.select(root)

            if n.state.is_terminal():
                value = n.state.get_value()
            else:
                n = MCTS.expand(n)
                value = MCTS.simulate(n)
            
            # if value < 0:
            #     value = value * 10
            #     print('aft: ', value)
            MCTS.backpropagate(n, value)
        
        # print('Tree:')
        # print(Node.print_graph(root))

        action_children = {child.action.idx: child.visit_count for child in root.children}
        action_space_counts = [(a, (action_children[a.idx] if a.idx in action_children else 0)) 
                                for a in root.state.available_actions()]
        total_visits = sum([a[1] for a in action_space_counts])
        total_visits = 1
        action_space_probs = [(a[0], a[1]/total_visits) for a in action_space_counts]
        return action_space_probs
        