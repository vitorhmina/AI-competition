from itertools import product
import numpy as np
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State


class ProbabilityMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: MinesweeperState):
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        possible_actions = list(state.get_possible_actions())

        # Calculate mine probabilities for all cells
        probabilities = self.calculate_probabilities(grid, num_rows, num_cols)

        # Find the action with the lowest probability of hitting a mine
        safest_action = min(possible_actions, key=lambda action: probabilities[action.get_row(), action.get_col()])
        return safest_action

    def calculate_probabilities(self, grid, num_rows, num_cols):
        probabilities = np.full((num_rows, num_cols), 1.0)

        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] >= 0:
                    self.update_probabilities(grid, probabilities, row, col, num_rows, num_cols)

        return probabilities

    def update_probabilities(self, grid, probabilities, row, col, num_rows, num_cols):
        num_mines = grid[row][col]
        neighbors = [(r, c) for r in range(max(0, row - 1), min(num_rows, row + 2))
                             for c in range(max(0, col - 1), min(num_cols, col + 2))
                             if grid[r][c] == MinesweeperState.EMPTY_CELL]

        if neighbors:
            mine_probability = num_mines / len(neighbors)
            for r, c in neighbors:
                probabilities[r, c] = min(probabilities[r, c], mine_probability)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass

