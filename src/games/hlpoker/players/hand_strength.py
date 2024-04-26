from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State

class HandStrengthHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        # Combine private cards and board cards to evaluate the hand
        all_cards = private_cards + board_cards

        if len(all_cards) >= 5:
            # Evaluate the hand only if we have at least 5 cards
            hand_strength = HLPokerState.evaluate_hand(all_cards)

            # Example decision-making logic based on hand strength
            if hand_strength > 0.5:
                if state.validate_action(HLPokerAction.RAISE):
                    return HLPokerAction.RAISE

        return HLPokerAction.CALL

    
    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass


