from game.roles import *

class Junior:
    def __init__(self, logger):
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
        self.logger = logger

    def on_turn(self, hand_cards, community_cards, pot, bet, opponents, poker):
        sorted_hand_cards = sort_cards_by_rank(hand_cards)
        format_card1 = format_card(sorted_hand_cards[0])
        format_card2 = format_card(sorted_hand_cards[1])
        hand_pair = '%s%s' % (format_card1[0], format_card2[0])
        try:
            self.BIG_PAIRS.index(hand_pair)
            return DECISION_CALL
        except ValueError:
            return DECISION_FOLD
