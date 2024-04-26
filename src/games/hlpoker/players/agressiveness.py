from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State

# Player based on hand strength and opponent aggressiveness
class AgressivenessHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.__hand_strength_threshold = 0.6
        self.__opponent_aggressiveness = 0.5

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        # Combine private cards and board cards to evaluate the hand
        all_cards = private_cards + board_cards

        if len(all_cards) >= 5:
            # Evaluate the hand only if we have at least 5 cards
            hand_strength = HLPokerState.evaluate_hand(all_cards)

            # Determine action based on hand strength and game state
            if hand_strength > self.__hand_strength_threshold:
                # Consider raising with a strong hand
                if state.validate_action(HLPokerAction.RAISE):
                    return HLPokerAction.RAISE

            # Adjust strategy based on opponent's aggressiveness
            if state.get_acting_player() == 1:  # Opponent's turn
                if self.__opponent_aggressiveness > 0.5:
                    # Opponent is aggressive, respond cautiously
                    if hand_strength > 0.4:
                        return HLPokerAction.CALL
                    else:
                        return HLPokerAction.FOLD
                else:
                    # Opponent is less aggressive, play more aggressively
                    if state.validate_action(HLPokerAction.RAISE):
                        return HLPokerAction.RAISE

        # Default action is to call if conditions are not met
        return HLPokerAction.CALL

    def event_my_action(self, action, new_state):
        # Implement strategy updates based on player's actions
        pass

    def event_opponent_action(self, action, new_state):
        # Update opponent modeling based on opponent's actions
        if action == HLPokerAction.RAISE:
            self.__opponent_aggressiveness += 0.1  # Increase aggressiveness perception
        elif action == HLPokerAction.FOLD:
            self.__opponent_aggressiveness -= 0.1  # Decrease aggressiveness perception

        # Ensure aggressiveness perception stays within reasonable bounds
        self.__opponent_aggressiveness = max(0, min(1, self.__opponent_aggressiveness))

    def event_new_game(self):
        # Reset player-specific parameters at the start of a new game
        self.__opponent_aggressiveness = 0.5

    def event_end_game(self, final_state: State):
        # Perform any final calculations or cleanup after the game ends
        pass

    def event_result(self, pos: int, result: int):
        # Update player's strategy or perception based on game result
        pass

    def event_new_round(self, round: Round):
        # Handle strategy adjustments at the start of a new game round
        pass
