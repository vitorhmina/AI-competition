from games.connect4.action import Connect4Action
from games.connect4.result import Connect4Result
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State
from math import inf
import random

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=4):
        super().__init__(name)
        self.max_depth = depth

    def get_action(self, state: Connect4State):
        _, action = self.minimax(state, self.max_depth, -inf, inf, True)
        return action

    def minimax(self, state: Connect4State, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_finished():
            return self.evaluate_state(state), None

        if maximizing_player:
            max_eval = -inf
            best_action = None
            for action in state.get_possible_actions():
                cloned_state = state.clone()
                cloned_state.update(action)
                eval_child, _ = self.minimax(cloned_state, depth - 1, alpha, beta, False)
                if eval_child > max_eval:
                    max_eval = eval_child
                    best_action = action
                alpha = max(alpha, eval_child)
                if beta <= alpha:
                    break
            return max_eval, best_action
        else:
            min_eval = inf
            best_action = None
            for action in state.get_possible_actions():
                cloned_state = state.clone()
                cloned_state.update(action)
                eval_child, _ = self.minimax(cloned_state, depth - 1, alpha, beta, True)
                if eval_child < min_eval:
                    min_eval = eval_child
                    best_action = action
                beta = min(beta, eval_child)
                if beta <= alpha:
                    break
            return min_eval, best_action

    def evaluate_state(self, state: Connect4State):
        if state.is_finished():
            result = state.get_result(self.get_current_pos())
            if result == Connect4Result.WIN.value:
                return 1000
            elif result == Connect4Result.LOOSE.value:
                return -1000
            else:
                return 0
        score = 0
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        player = self.get_current_pos()

        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == player:
                    # Check vertical
                    if row <= num_rows - 4:
                        if grid[row + 1][col] == player and grid[row + 2][col] == player and grid[row + 3][col] == player:
                            score += 100
                    # Check horizontal
                    if col <= num_cols - 4:
                        if grid[row][col + 1] == player and grid[row][col + 2] == player and grid[row][col + 3] == player:
                            score += 100
                    # Check diagonal (bottom-left to top-right)
                    if row <= num_rows - 4 and col >= 3:
                        if grid[row + 1][col - 1] == player and grid[row + 2][col - 2] == player and grid[row + 3][col - 3] == player:
                            score += 100
                    # Check diagonal (top-left to bottom-right)
                    if row <= num_rows - 4 and col <= num_cols - 4:
                        if grid[row + 1][col + 1] == player and grid[row + 2][col + 2] == player and grid[row + 3][col + 3] == player:
                            score += 100
        return score

    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        pass
