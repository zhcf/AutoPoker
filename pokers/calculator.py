import role_utils as utils
import random
import itertools

class Calculator:
    def __init__(self):
        self.STARTUP_STRENGTH = (1.0, 0.5, 0.25, 0)
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

    def on_turn(self, hand_cards, river_cards, pot, bet, players, poker):
        if bet == 0:
            return utils.DECISION_CALL
        hand_strength = get_hand_strength()
        pot_odds = bet / (pot + bet)
        rate_of_return = hand_strengh / pot_odds
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

    def get_hand_strength(self, hand_cards, river_cards, number_of_players, try_times):
        times = 0
        win_times = 0
        while times <= try_times:
            # Shuffle the deck
            deck = random.sample(range(52),k=52)
            # Remove the cards that already deal to poker
            for card in hand_cards:
                deck.remove(card)
            # Remove the cards that already deal to river
            for card in river_cards:
                deck.remove(card)
            # Deal cards to Players
            players_hand_cards = []
            for i in range(number_of_players):
                players_hand_cards.append((deck.pop(), deck.pop()))
            # Get combination of river cards
            poker_hand_values = []
            player_hand_values = []
            for cards in itertools.combinations(river_cards, 3):
                hand_value = utils.get_hand_value(list(hand_cards) + list(cards))
                poker_hand_values.append(hand_value)
                for player_hand_cards in players_hand_cards:
                    hand_value = utils.get_hand_value(player_hand_cards + cards)
                    player_hand_values.append(hand_value)
            if max(poker_hand_values) > max(player_hand_values):
                win_times = win_times + 1
            times = times + 1
        return win_times / times

    def __get_pot_odds():
        pass
