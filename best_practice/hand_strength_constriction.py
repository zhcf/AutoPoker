import sys
sys.path.append("..")
import role_utils as utils
import random
import itertools
import math

ROYAL_FLUSH = ['TS', 'JS', 'QS', 'KS', 'AS']
STRAIGHT_FLUSH = ['5C', '6C', '7C', '8C', '9C']
FOUR_OF_A_KIND = ['8C', 'AD', 'AC', 'AS', 'AH']
FULL_HOUSE = ['KC', 'KH', 'KS', 'TC', 'TS']
FLUSH = ['QC', '8C', '6C', '4C', '3C']
STRAIGHT = ['2D', '3C', '4S', '5D', '6S']
THREE_OF_A_KIND = ['JD', 'JC', 'JH', '5C', '8D']
HT_TWO_PAIR = ['6S', '6C', 'TC', 'TD', 'KD']
ONE_PAIR = ['2D', '6H', '8S', 'AC', 'AH']
HIGH_CARD = ['KH', 'JS', 'TC', '6H','3D']

if __name__=='__main__':
    hand_cards = utils.parse_cards(FLUSH[3:])
    community_cards = utils.parse_cards(FLUSH[:3])
    number_of_opponents = 1
    try_times = math.pow(100, 4)
    times = 0
    win_times = 0
    log_times = 100
    while times <= try_times:
        # Shuffle the deck
        deck = random.sample(range(52),k=52)
        # Remove the cards that already deal to poker
        for card in hand_cards:
            deck.remove(card)
        # Remove the cards that already deal to river
        for card in community_cards:
            deck.remove(card)
        # Fill community card to five
        temp_community_cards = []
        for i in range(5):
            if i < len(community_cards):
                temp_community_cards.append(community_cards[i])
            else:
                temp_community_cards.append(deck.pop())
        # Deal cards to Players
        opponents_hand_cards = []
        for i in range(number_of_opponents):
            opponents_hand_cards.append((deck.pop(), deck.pop()))
        #print(opponents_hand_cards)
        # Get combination of river cards
        poker_hand_values = []
        opponent_hand_values = []
        for cards in itertools.combinations(temp_community_cards, 3):
            hand_value = utils.get_hand_value(list(hand_cards) + list(cards))
            #print("Poker:%d" % hand_value)
            poker_hand_values.append(hand_value)
            for opponent_hand_cards in opponents_hand_cards:
                hand_value = utils.get_hand_value(opponent_hand_cards + cards)
                #print("Opponent:%d" % hand_value)
                opponent_hand_values.append(hand_value)
        if max(poker_hand_values) > max(opponent_hand_values):
            win_times = win_times + 1
        times = times + 1
        if times % log_times == 0:
            print("%d,%f" % (times, win_times / times))
