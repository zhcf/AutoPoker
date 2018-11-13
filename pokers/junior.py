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

    def on_turn(self, hand_cards, river_cards, pot):
        sorted_hand_cards = utils.sort_cards_by_rank(hand_cards)
        format_card1 = utils.format_card(sorted_hand_cards[0])
        format_card2 = utils.format_card(sorted_hand_cards[1])
        hand_pair = '%s%s' % (format_card1[0], format_card2[0])
        try:
            self.BIG_PAIRS.index(hand_pair)
            return utils.DECISION_CALL
        except ValueError:
            return utils.DECISION_FOLD
