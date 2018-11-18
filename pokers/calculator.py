import role_utils as utils
import random
import itertools

class Calculator:
    def __init__(self, logger):
        self.STARTUP_HOLD_POSITIONS = (
            ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'],
            ['MP', 'CO', 'BTN'],
            ['CO', 'BTN'],
            []
        )
        self.STARTUP_PAIR = ( ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77'], ['66', '55'], ['44', '33', '22'], [] )
        self.STARTUP_SAME_SUIT = [
            ( ['AK', 'AQ', 'AJ', 'AT'], ['A9', 'A8', 'A7', 'A6'], ['A5', 'A4', 'A3', 'A2'], [] ),
            ( ['KQ', 'KJ', 'KT'], ['K9'], ['K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2'], [] ),
            ( ['QJ', 'QT'], ['Q9', 'Q8'], [], ['Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2'] ),
            ( ['JT', 'J9'], ['J8'], ['J7'], ['J6', 'J5', 'J4', 'J3', 'J2'] ),
            ( ['T9'], ['T8'], ['T7'], ['T6', 'T5', 'T4', 'T3', 'T2'] ),
            ( [], ['98'], ['97', '96'], ['95', '94', '93', '92'] ),
            ( [], [], ['87', '86'], ['85', '84', '83', '82']),
            ( [], [], ['76', '75'], ['74', '73', '72']),
            ( [], [], ['65'], ['64', '63', '62']),
            ( [], [], ['54'], ['53', '52']),
            ( [], [], [], ['43', '42']),
            ( [], [], [], ['32'])
        ]
        self.STARTUP_NO_SAME_SUIT = [
            ( ['AK', 'AQ', 'AJ', 'AT'], [], ['A9', 'A8', 'A7'], ['A6', 'A5', 'A4', 'A3', 'A2'] ),
            ( ['KQ', 'KJ'], ['KT'], ['K9'], ['K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2'] ),
            ( [], ['QJ', 'QT'], ['Q9'], ['Q8', 'Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2'] ),
            ( [], ['JT'], ['J9', 'J8'], ['J7', 'J6', 'J5', 'J4', 'J3', 'J2'] ),
            ( [], [], ['T9', 'T8'], ['T7', 'T6', 'T5', 'T4', 'T3', 'T2'] ),
            ( [], [], ['98', '97'], ['96', '95', '94', '93', '92'] ),
            ( [], [], ['87'], ['86', '85', '84', '83', '82']),
            ( [], [], [], ['76', '75', '74', '73', '72']),
            ( [], [], [], ['65', '64', '63', '62']),
            ( [], [], [], ['54', '53', '52']),
            ( [], [], [], ['43', '42']),
            ( [], [], [], ['32'])
        ]
        self.DEFAULT_TRY_TIMES = 1000
        self.logger = logger

    def on_turn(self, hand_cards, community_cards, pot, bet, opponents, poker):
        if bet == 0:
            return utils.DECISION_CALL
        if len(community_cards) <= 2:
            hold_positions = self.get_startup_hold_positions(hand_cards)
            try:
                hold_positions.index(poker.position[0])
                return utils.DECISION_CALL
            except ValueError as e:
                return utils.DECISION_FOLD
        else:
            hand_strength = self.get_hand_strength(hand_cards, community_cards, len(opponents), self.DEFAULT_TRY_TIMES)
        pot_odds = bet / (pot + bet)
        rate_of_return = hand_strength / pot_odds
        self.logger.info("STR:%f, ODDS=%f, ROR=%f" % (hand_strength, pot_odds, rate_of_return))
        return self.__make_decision(rate_of_return)

    def __make_decision(self, rate_of_return):
        bluff_rate = random.random()
        if rate_of_return < 0.8:
            if bluff_rate <= 0.95:
                return utils.DECISION_FOLD
            else:
                return utils.DECISION_RAISE
        elif rate_of_return < 1.0:
            if bluff_rate <= 0.80:
                return utils.DECISION_FOLD
            elif bluff_rate <= 0.85:
                return utils.DECISION_CALL
            else:
                return utils.DECISION_RAISE
        elif rate_of_return < 1.3:
            if bluff_rate <= 0.60:
                return utils.DECISION_CALL
            else:
                return utils.DECISION_RAISE
        else:
            if bluff_rate <= 0.30:
                return utils.DECISION_CALL
            else:
                return utils.DECISION_RAISE

    def get_startup_hold_positions(self, hand_cards):
        assert len(hand_cards) == 2
        sorted_hand_cards = utils.sort_cards_by_rank(hand_cards)
        (suit1, rank1) = utils.split_card(sorted_hand_cards[0])
        (suit2, rank2) = utils.split_card(sorted_hand_cards[1])
        if rank1 == rank2:
            mappings = [self.STARTUP_PAIR]
        elif suit1 == suit2:
            mappings = self.STARTUP_SAME_SUIT
        else:
            mappings = self.STARTUP_NO_SAME_SUIT
        for mapping in mappings:
            section_index = 0
            for define_ranks_list in mapping:
                for define_ranks in define_ranks_list:
                    define_rank1 = utils.parse_rank(define_ranks[0])
                    define_rank2 = utils.parse_rank(define_ranks[1])
                    if define_rank1 == rank1 and define_rank2 == rank2:
                        return self.STARTUP_HOLD_POSITIONS[section_index]
                section_index = section_index + 1
        return None

    def get_hand_strength(self, hand_cards, community_cards, number_of_opponents, try_times):
        times = 0
        win_times = 0
        while times <= try_times:
            # Shuffle the deck
            deck = random.sample(range(52),k=52)
            # Remove the cards that already deal to poker
            for card in hand_cards:
                deck.remove(card)
            # Remove the cards that already deal to river
            for card in community_cards:
                deck.remove(card)
            # Deal cards to Players
            opponents_hand_cards = []
            for i in range(number_of_opponents):
                opponents_hand_cards.append((deck.pop(), deck.pop()))
            # Get combination of river cards
            poker_hand_values = []
            opponent_hand_values = []
            for cards in itertools.combinations(community_cards, 3):
                hand_value = utils.get_hand_value(list(hand_cards) + list(cards))
                poker_hand_values.append(hand_value)
                for opponent_hand_cards in opponents_hand_cards:
                    hand_value = utils.get_hand_value(opponent_hand_cards + cards)
                    opponent_hand_values.append(hand_value)
            if max(poker_hand_values) > max(opponent_hand_values):
                win_times = win_times + 1
            times = times + 1
        return win_times / times

    def __get_pot_odds():
        pass
