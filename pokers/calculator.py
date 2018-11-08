import role_utils as utils

class Junior:
    def __init__(self):
        pass

    def on_turn(self, hand_cards, table_cards, pot, call_amount, raise_amount):
        hand_strengh = __get_hand_strengh()
        pot_odds = __get_pot_odds()
        rate_of_return = hand_strengh / pot_odds
        pass

    def __get_hand_strengh():
        pass

    def __get_pot_odds():
        pass
