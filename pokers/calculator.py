import role_utils as utils
import random
import itertools

class Calculator:
    def __init__(self):
        pass

    def on_turn(self, hand_cards, river_cards, pot, players, poker):
        hand_strengh = __get_hand_strengh()
        pot_odds = __get_pot_odds()
        rate_of_return = hand_strengh / pot_odds
        pass

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
