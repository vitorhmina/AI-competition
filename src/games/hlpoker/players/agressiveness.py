from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State

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

            # If the hand is strong raise
            if hand_strength > self.__hand_strength_threshold:
                if state.validate_action(HLPokerAction.RAISE):
                    return HLPokerAction.RAISE

            if state.get_acting_player() == 1:
                if self.__opponent_aggressiveness > 0.5:
                    # Opponent is aggressive, respond accordingly
                    if hand_strength > 0.4:
                        return HLPokerAction.CALL
                    else:
                        return HLPokerAction.FOLD
                else:
                    # Opponent is less aggressive, play more aggressively
                    if state.validate_action(HLPokerAction.RAISE):
                        return HLPokerAction.RAISE

        # Default action is to call
        return HLPokerAction.CALL

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        # Update opponent aggressivness based on it's actions
        if action == HLPokerAction.RAISE:
            self.__opponent_aggressiveness += 0.1
        elif action == HLPokerAction.FOLD:
            self.__opponent_aggressiveness -= 0.1

        # Make sure opponent aggressivness stays between 0 and 1
        self.__opponent_aggressiveness = max(0, min(1, self.__opponent_aggressiveness))

    def event_new_game(self):
        self.__opponent_aggressiveness = 0.5

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass
