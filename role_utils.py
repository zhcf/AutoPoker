import functools

SUIT_HEART = 0
SUIT_SPADE = 1
SUIT_CLUB = 2
SUIT_DIAMOND = 3

SUIT_MAPPINGS = [
    (SUIT_HEART, 'H'),
    (SUIT_SPADE, 'S'),
    (SUIT_CLUB, 'C'),
    (SUIT_DIAMOND, 'D')
]

RANK_A = 12
RANK_K = 11
RANK_Q = 10
RANK_J = 9
RANK_T = 8
RANK_9 = 7
RANK_8 = 6
RANK_7 = 5
RANK_6 = 4
RANK_5 = 3
RANK_4 = 2
RANK_3 = 1
RANK_2 = 0

RANK_MAPPINGS = [
    (RANK_A, 'A'),
    (RANK_K, 'K'),
    (RANK_Q, 'Q'),
    (RANK_J, 'J'),
    (RANK_T, 'T'),
    (RANK_9, '9'),
    (RANK_8, '8'),
    (RANK_7, '7'),
    (RANK_6, '6'),
    (RANK_5, '5'),
    (RANK_4, '4'),
    (RANK_3, '3'),
    (RANK_2, '2')
]

HT_ROYAL_FLUSH = 9
HT_STRAIGHT_FLUSH = 8
HT_FOUR_OF_A_KIND = 7
HT_FULL_HOUSE = 6
HT_FLUSH = 5
HT_STRAIGHT = 4
HT_THREE_OF_A_KIND = 3
HT_TWO_PAIR = 2
HT_ONE_PAIR = 1
HT_HIGH_CARD = 0

DECISION_FOLD = 'fold'
DECISION_CALL = 'call'
DECISION_RAISE = 'raise'

POSITION_SB = 'SB'
POSITION_BB = 'BB'
POSITION_UTG = 'UTG'
POSITION_MP = 'MP'
POSITION_CO = 'CO'
POSITION_BTN = 'BTN'

def sort_actions(actions):
    return sorted(actions, key=functools.cmp_to_key(__action_cmp))

def __action_cmp(a1, a2):
    return compare_action(a1.action, a2.action)

def compare_action(a1, a2):
    values = ['fold', 'check', 'call', 'bet', 'raise']
    idx1 = values.index(a1)
    idx2 = values.index(a2)
    if idx1 > idx2:
        return 1
    if idx1 < idx2:
        return -1
    return 0

def split_card(card):
    suit = int(card / 13)
    rank = card % 13
    return (suit, rank)

def get_card(suit, rank):
    return suit * 13 + rank

def parse_card(card_str):
    rank = parse_rank(card_str[0])
    suit = parse_suit(card_str[1])
    if rank is None or suit is None:
        return None
    else:
        return get_card(suit, rank)

def parse_cards(card_str_list):
    cards = []
    for card_str in card_str_list:
        cards.append(parse_card(card_str))
    return cards

def parse_rank(rank_char):
    for mapping in RANK_MAPPINGS:
        if mapping[1] == rank_char:
            return mapping[0]
    return None

def parse_suit(suit_char):
    for mapping in SUIT_MAPPINGS:
        if mapping[1] == suit_char:
            return mapping[0]
    return None

def format_card(card):
    (suit, rank) = split_card(card)
    for mapping in RANK_MAPPINGS:
        if mapping[0] == rank:
            rank_str = mapping[1]
            break
    for mapping in SUIT_MAPPINGS:
        if mapping[0] == suit:
            suit_str = mapping[1]
            break
    return '%s%s' % (rank_str, suit_str)

def sort_cards_by_rank(cards):
    return sorted(cards, key=functools.cmp_to_key(__card_rank_cmp))

def __card_rank_cmp(card1, card2):
    (suit1, rank1) = split_card(card1)
    (suit2, rank2) = split_card(card2)
    if rank1 < rank2:
        return 1
    if rank1 > rank2:
        return -1
    return 0

def get_hand_value(cards):
    assert len(cards) == 5
    sorted_cards = sort_cards_by_rank(cards)
    hand_type = get_hand_type(cards, sorted = True)
    hand_value = hand_type * 100 * 100 * 100 * 100 * 100 + \
        sorted_cards[0] * 100 * 100 * 100 * 100 + \
        sorted_cards[1] * 100 * 100 * 100 + \
        sorted_cards[2] * 100 * 100 + \
        sorted_cards[3] * 100 + \
        sorted_cards[4]
    return hand_value

def get_hand_type(cards, sorted = False):
    assert len(cards) == 5
    if not sorted:
        sorted_cards = sort_cards_by_rank(cards)
    else:
        sorted_cards = cards
    hand_types = []
    suit_dict = dict()
    rank_dict = dict()
    straight = None
    for card in sorted_cards:
        (suit, rank) = split_card(card)
        # Summary by suit
        if suit not in suit_dict:
            suit_dict[suit] = {
                'count': 1,
                'straight': [rank]
            }
        else:
            suit_dict[suit]['count'] = suit_dict[suit]['count'] + 1
            if len(suit_dict[suit]['straight']) < 5:
                if rank == suit_dict[suit]['straight'][-1] - 1:
                    suit_dict[suit]['straight'].append(rank)
                elif rank != suit_dict[suit]['straight'][-1]:
                    suit_dict[suit]['straight'] = [rank]
        # Summary by rank
        if rank not in rank_dict:
            rank_dict[rank] = 1
        else:
            rank_dict[rank] = rank_dict[rank] + 1
        # Looking for max straight
        if straight is None:
            straight = [rank]
        elif len(straight) < 5:
            if rank == straight[-1] - 1:
                straight.append(rank)
            elif rank != straight[-1]:
                straight = [rank]
    # Looking for available hand type
    for k, v in suit_dict.items():
        if v['count'] >= 5:
            if len(v['straight']) >= 5:
                if v['straight'][0] == RANK_A:
                    hand_types.append(HT_ROYAL_FLUSH)
                else:
                    hand_types.append(HT_STRAIGHT_FLUSH)
            else:
                hand_types.append(HT_FLUSH)
    if len(straight) >= 5:
        hand_types.append(HT_STRAIGHT)
    pair_count = 0
    three_count = 0
    four_count = 0
    for k, v in rank_dict.items():
        if v >= 4:
            four_count = four_count + 1
        elif v >= 3:
            three_count = three_count + 1
        elif v >= 2:
            pair_count = pair_count + 1
    if four_count >= 1:
        hand_types.append(HT_FOUR_OF_A_KIND)
    elif three_count >= 1:
        if pair_count >= 1:
            hand_types.append(HT_FULL_HOUSE)
        else:
            hand_types.append(HT_THREE_OF_A_KIND)
    elif pair_count > 0:
        if pair_count >= 2:
            hand_types.append(HT_TWO_PAIR)
        else:
            hand_types.append(HT_ONE_PAIR)
    else:
        hand_types.append(HT_HIGH_CARD)
    # Use the max hand type
    return max(hand_types)

def get_player_positions(table_size):
    assert table_size == 6 or table_size == 9
    if table_size == 6:
        return [
            (POSITION_SB, 0),
            (POSITION_BB, 0),
            (POSITION_UTG, 0),
            (POSITION_MP, 0),
            (POSITION_CO, 0),
            (POSITION_BTN, 0)
        ]
    if table_size == 9:
        return [
            (POSITION_SB, 0),
            (POSITION_BB, 0),
            (POSITION_UTG, 0),
            (POSITION_UTG, 1),
            (POSITION_MP, 0),
            (POSITION_MP, 1),
            (POSITION_MP, 2),
            (POSITION_CO, 0),
            (POSITION_BTN, 0)
        ]
