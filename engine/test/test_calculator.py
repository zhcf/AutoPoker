from game.roles import *
from pokers import create_poker
import logging

class TestGamePlayer():
    pass

def test_get_startup_hand_strength():
    scenario_list = [
        ( ['TS', 'JS'], 'UTG', DECISION_CALL ),
        ( ['6C', '6S'], 'UTG', DECISION_FOLD ),
        ( ['8D', '7C'], 'BTN', DECISION_CALL ),
        ( ['4H', '2D'], 'BTN', DECISION_FOLD )
    ]
    calculator = create_poker('calculator', logging.getLogger(''))
    for scenario in scenario_list:
        poker = TestGamePlayer()
        poker.code = 'poker'
        poker.position = (scenario[1], 0)
        poker.balance = 100
        decision = calculator.on_turn(hand_cards = parse_cards(scenario[0]),
            community_cards = [],
            pot = 100,
            bet = 50,
            opponents = [],
            poker = poker)
        assert decision == scenario[2]

def test_get_hand_strength():
    calculator = create_poker('calculator', logging.getLogger(''))
    hand_cards = parse_cards(['TS', 'JS'])
    community_cards = parse_cards(['QS', 'KS', 'AS', '3D', '4H'])
    strength = calculator.get_hand_strength(hand_cards, community_cards, 5, 1000)
    assert strength == 1
