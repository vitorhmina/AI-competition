from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.minesweeper.action import MinesweeperAction
import math

class MinimaxMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name, max_depth=5):
        super().__init__(name)
        self.max_depth = max_depth

    def get_action(self, state: MinesweeperState) -> MinesweeperAction:
        best_action = self.minimax(state, self.max_depth, True, -math.inf, math.inf)[1]
        return best_action

    def minimax(self, state: MinesweeperState, depth, maximizing_player, alpha, beta):
        if depth == 0 or state.is_finished():
            return self.evaluate_state(state), None

        possible_actions = list(state.get_possible_actions())

        if maximizing_player:
            max_eval = -math.inf
            best_action = None
            for action in possible_actions:
                new_state = state.clone()
                new_state.update(action)
                eval = self.minimax(new_state, depth - 1, False, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_action
        else:
            min_eval = math.inf
            best_action = None
            for action in possible_actions:
                new_state = state.clone()
                new_state.update(action)
                eval = self.minimax(new_state, depth - 1, True, alpha, beta)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_action = action
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_action

    def evaluate_state(self, state: MinesweeperState):
        # Example evaluation function based on game progress and revealed cells
        num_revealed_cells = sum(1 for row in state.get_grid() for cell in row if cell != MinesweeperState.EMPTY_CELL)
        total_cells = state.get_num_rows() * state.get_num_cols()
        progress_score = num_revealed_cells / total_cells

        if state.is_finished():
            result = state.get_result(0)
            if result == 1:
                return 100  # Winning state
            elif result == -1:
                return -100  # Losing state
        else:
            return progress_score * 100  # Intermediate state evaluation

    def event_action(self, pos: int, action, new_state: MinesweeperState):
        # Ignore action events for the AI player
        pass

    def event_end_game(self, final_state: MinesweeperState):
        # Ignore end game events for the AI player
        pass