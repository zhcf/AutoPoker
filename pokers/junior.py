import role_utils as utils

class Junior:
    def __init__(self):
        self.BIG_PAIRS = ['AA',
            'KK',
            'QQ',
            'JJ',
            'TT',
            '99',
            '88',
            '77',
            'AK',
            'AQ']

    def on_turn(self, hand_cards, table_cards, pot):
        sorted_hand_cards = utils.sort_cards_by_value(hand_cards)
        hand_pair = '%s%s' % (sorted_hand_cards[0][0], sorted_hand_cards[1][0])
        try:
            self.BIG_PAIRS.index(hand_pair)
            return 'bet'
        except ValueError:
            return 'fold'
