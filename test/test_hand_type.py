import role_utils as utils

def __get_hand_type(card_strs):
    cards = []
    for str in card_strs:
        card = utils.parse_card(str)
        cards.append(card)
    return utils.get_hand_type(cards)

def test_royal_flush():
    cards = ['TS', 'JS', 'QS', 'KS', 'AS']
    assert __get_hand_type(cards) == utils.HT_ROYAL_FLUSH

def test_straight_flush():
    cards = ['5C', '6C', '7C', '8C', '9C']
    assert __get_hand_type(cards) == utils.HT_STRAIGHT_FLUSH

def test_four_of_a_kind():
    cards = ['8C', 'AD', 'AC', 'AS', 'AH']
    assert __get_hand_type(cards) == utils.HT_FOUR_OF_A_KIND

def test_full_house():
    cards = ['KC', 'KH', 'KS', 'TC', 'TS']
    assert __get_hand_type(cards) == utils.HT_FULL_HOUSE

def test_flush():
    cards = ['QC', '8C', '6C', '4C', '3C']
    assert __get_hand_type(cards) == utils.HT_FLUSH

def test_straight():
    cards = ['2D', '3C', '4S', '5D', '6S']
    assert __get_hand_type(cards) == utils.HT_STRAIGHT

def test_three_of_a_kind():
    cards = ['JD', 'JC', 'JH', '5C', '8D']
    assert __get_hand_type(cards) == utils.HT_THREE_OF_A_KIND

def test_two_pair():
    cards = ['6S', '6C', 'TC', 'TD', 'KD']
    assert __get_hand_type(cards) == utils.HT_TWO_PAIR

def test_one_pair():
    cards = ['2D', '6H', '8S', 'AC', 'AH']
    assert __get_hand_type(cards) == utils.HT_ONE_PAIR

def test_high_card():
    cards = ['KH', 'JS', 'TC', '6H','3D']
    assert __get_hand_type(cards) == utils.HT_HIGH_CARD
