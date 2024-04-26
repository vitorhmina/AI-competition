import random
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState

class MonteCarloMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name, num_simulations=100):
        super().__init__(name)
        self.num_simulations = num_simulations

    def get_action(self, state: MinesweeperState):
        # Get the game grid and dimensions
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()

        # Perform Monte Carlo simulations to estimate the probability of each action
        action_probabilities = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]

        for _ in range(self.num_simulations):
            # Simulate a random sequence of actions
            simulated_state = state.clone()
            while not simulated_state.is_finished():
                possible_actions = list(simulated_state.get_possible_actions())
                if possible_actions:
                    random_action = random.choice(possible_actions)
                    simulated_state.update(random_action)

            # Update action probabilities based on the simulation result
            for row in range(num_rows):
                for col in range(num_cols):
                    if grid[row][col] == MinesweeperState.EMPTY_CELL:
                        if simulated_state.get_grid()[row][col] == MinesweeperState.EMPTY_CELL:
                            action_probabilities[row][col] += 1

        # Find the action with the highest probability of being safe
        max_probability = -1
        best_action = MinesweeperAction(0, 0)

        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == MinesweeperState.EMPTY_CELL:
                    probability = action_probabilities[row][col] / self.num_simulations
                    if probability > max_probability:
                        max_probability = probability
                        best_action = MinesweeperAction(row, col)

        return best_action

    def event_action(self, pos: int, action, new_state: MinesweeperState):
        # Ignore action events for the Monte Carlo player
        pass

    def event_end_game(self, final_state: MinesweeperState):
        # Ignore end game events for the Monte Carlo player
        pass
