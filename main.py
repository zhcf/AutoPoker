from gui_element import *
from gui_control import *
from game_table import *
import time
import sys

window_rect = find_in_screen(WINDOW_TOP_LEFT)
if window_rect is None:
    print("No game window")
    sys.exit(1)
window_rect.h = WINDOW_HEIGHT
window_rect.w = WINDOW_WIDTH
print("Game window found: %s" % window_rect.to_string())

table_rect = find_in_rect(TABLE_TOP_LEFT, window_rect)
if table_rect is None:
    print("No game table")
    sys.exit(1)
table_rect.h = TABLE_HEIGHT
table_rect.w = TABLE_WIDTH
print("Game table found: %s" % table_rect.to_string())

while True:
    cmd = input("Input something to continue...")
    if cmd == 'exit':
        break
    t1 = time.time()
    table = GameTable(table_rect)
    actions = table.get_avail_actions()
    print("Action:")
    for action in actions:
        print(action.to_string())

    (table_cards, hand_cards) = table.get_cards()
    print("Table cards:")
    for card in table_cards:
        print(card)
    print("Hand cards:")
    for card in hand_cards:
        print(card)
    t2 = time.time()
    print("Time pass: %f" % (t2 - t1))

# card_anchors = find_all_in_rect(CARD_ANCHOR, table_rect)
# print(card_anchors)
