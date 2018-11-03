from gui_element import *
from gui_control import *
from game_table import *

window_rect = find_in_screen(WINDOW_TOP_LEFT)
window_rect.h = WINDOW_HEIGHT
window_rect.w = WINDOW_WIDTH
print(window_rect.to_string())

table_rect = find_in_rect(TABLE_TOP_LEFT, window_rect)
table_rect.h = TABLE_HEIGHT
table_rect.w = TABLE_WIDTH
print(table_rect.to_string())

table = GameTable(table_rect)
actions = table.get_avail_actions()
for action in actions:
    print(action.to_string())

hand_cards = table.get_hand_cards()
for card in hand_cards:
    print(card)

# card_anchors = find_all_in_rect(CARD_ANCHOR, table_rect)
# print(card_anchors)
