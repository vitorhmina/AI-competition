import numpy as np
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State
import random

class QLearningConnect4Player(Connect4Player):
    def __init__(self, name, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        super().__init__(name)
        self.learning_rate = learning_rate  # Q-learning rate
        self.discount_factor = discount_factor  # Discount factor for future rewards
        self.exploration_rate = exploration_rate  # Exploration rate (epsilon-greedy)
        self.q_values = {}  # Dictionary to store Q-values for state-action pairs

    def get_action(self, state: Connect4State):
        if random.random() < self.exploration_rate:
            # Explore: choose a random action
            return random.choice(state.get_possible_actions())

        # Exploit: choose the action with the highest Q-value
        best_action = None
        best_q_value = -float('inf')
        for action in state.get_possible_actions():
            q_value = self.get_q_value(state, action)
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action
        
        return best_action

    def get_q_value(self, state, action):
        # Retrieve Q-value for a state-action pair; initialize to zero if unseen
        state_key = self.get_state_key(state)
        return self.q_values.get((state_key, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        # Update Q-value using the Q-learning update rule
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        current_q_value = self.get_q_value(state, action)
        max_next_q_value = max([self.get_q_value(next_state, next_action) for next_action in next_state.get_possible_actions()])
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)
        self.q_values[(state_key, action)] = new_q_value

    def get_state_key(self, state):
        # Generate a unique key for a Connect4State object (used for Q-value dictionary)
        return str(state.get_grid())

    def event_end_game(self, final_state: Connect4State):
        # Update Q-values based on game outcome (reward)
        winner = final_state.get_result(self.get_current_pos())
        reward = 1.0 if winner == 1 else -1.0  # Reward: +1 for winning, -1 for losing
        self.update_q_values(reward)

    def update_q_values(self, reward):
        # Update Q-values for all state-action pairs encountered in the current game
        visited_states = set()
        for (state_action_key, _), q_value in self.q_values.items():
            state_key, action = state_action_key
            if state_key not in visited_states:
                visited_states.add(state_key)
                q_value += self.learning_rate * (reward - q_value)
                self.q_values[(state_key, action)] = q_value

    def event_action(self, pos: int, action, new_state: State):
        # Implement if needed
        pass

    def event_end_game(self, final_state: State):
        # Implement if needed
        pass
