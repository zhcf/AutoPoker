import role_utils as utils
import random

class Junior:
    def __init__(self):
        pass

    def on_turn(self, hand_cards, river_cards, pot, players, poker):
        hand_strengh = __get_hand_strengh()
        pot_odds = __get_pot_odds()
        rate_of_return = hand_strengh / pot_odds
        pass

    def __get_hand_strengh(hand_cards, river_cards, number_of_players, try_times):
        times = 0
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
            # Get

        pass


    def __get_pot_odds():
        pass
