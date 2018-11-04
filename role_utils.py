import functools

def sort_cards_by_value(cards):
    return sorted(cards, key=functools.cmp_to_key(__card_value_cmp))

def __card_value_cmp(c1, c2):
    values = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    idx1 = values.index(c1[0])
    idx2 = values.index(c2[0])
    if idx1 > idx2:
        return 1
    if idx1 < idx2:
        return -1
    return 0

def sort_actions(actions):
    return sorted(actions, key=functools.cmp_to_key(__action_cmp))

def __action_cmp(a1, a2):
    return compare_action(a1.action, a2.action)

def compare_action(a1, a2):
    values = ['fold', 'check', 'call', 'bet', 'raise_to']
    idx1 = values.index(a1)
    idx2 = values.index(a2)
    if idx1 > idx2:
        return 1
    if idx1 < idx2:
        return -1
    return 0
