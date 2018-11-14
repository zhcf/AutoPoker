import role_utils as utils
from pokers.calculator import Calculator

def test_get_hand_strength():
    calculator = Calculator()
    hand_cards = utils.parse_cards(['TS', 'JS'])
    river_cards = utils.parse_cards(['QS', 'KS', 'AS', '3D', '4H'])
    strength = calculator.get_hand_strength(hand_cards, river_cards, 5, 1000)
    assert strength == 1
