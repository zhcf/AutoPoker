import role_utils as utils
from pokers.calculator import Calculator

def test_get_startup_hand_strength():
    hand_cards_list = [
        ( ['TS', 'JS'], 1.0 ),
        ( ['6C', '6S'], 0.5 ),
        ( ['8D', '7C'], 0.25 ),
        ( ['4H', '2D'], 0)
    ]
    calculator = Calculator()
    for hand_cards in hand_cards_list:
        strength = calculator.get_startup_hand_strength(utils.parse_cards(hand_cards[0]))
        assert strength == hand_cards[1]

def test_get_hand_strength():
    calculator = Calculator()
    hand_cards = utils.parse_cards(['TS', 'JS'])
    community_cards = utils.parse_cards(['QS', 'KS', 'AS', '3D', '4H'])
    strength = calculator.get_hand_strength(hand_cards, community_cards, 5, 1000)
    assert strength == 1
