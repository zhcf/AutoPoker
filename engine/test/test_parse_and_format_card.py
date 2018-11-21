import role_utils as utils

def test_parse_and_format_card():
    cards =  ['TS', 'JS', 'QS', 'KS', 'AS', '5C', '6C', '7C', '8C', '9C', '8C', 'AD', 'AC', 'AS', 'AH', 'KC', 'KH', 'KS', 'TC', 'TS', 'QC', '8C', '6C', '4C', '3C', '2D', '3C', '4S', '5D', '6S', 'JD', 'JC', 'JH', '5C', '8D', '6S', '6C', 'TC', 'TD', 'KD', '2D', '6H', '8S', 'AC', 'AH', 'KH', 'JS', 'TC', '6H','3D']
    for card in cards:
        temp = utils.parse_card(card)
        cmp_card = utils.format_card(temp)
        assert card == cmp_card
