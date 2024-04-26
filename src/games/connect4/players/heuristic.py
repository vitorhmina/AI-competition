from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
import random

class HeuristicConnect4Player(Connect4Player):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: Connect4State):
        # Choose the best action based on a simple heuristic
        best_action = None
        best_score = -float('inf')

        for action in state.get_possible_actions():
            score = self.evaluate_action(state, action)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def evaluate_action(self, state: Connect4State, action: Connect4Action) -> float:
        # Evaluate the desirability of taking 'action' in 'state'
        cloned_state = state.clone()
        cloned_state.update(action)

        # Simple heuristic: prioritize moves that contribute to potential winning configurations
        return self.evaluate_state(cloned_state)

    def evaluate_state(self, state: Connect4State) -> float:
        # Evaluate the desirability of the current state for the current player
        current_player = state.get_acting_player()
        opponent_player = 1 - current_player

        # Example: Evaluate based on the number of pieces in potential winning configurations
        score = 0

        # Check horizontally
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row][col + i] for i in range(4)]
                if window.count(current_player) == 3 and window.count(state.EMPTY_CELL) == 1:
                    score += 1

        return score

    def event_action(self, pos: int, action, new_state: Connect4State):
        # Ignore
        pass

    def event_end_game(self, final_state: Connect4State):
        # Ignore
        pass
