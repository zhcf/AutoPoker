from gui_element import *
from gui_control import *
from game_table import *
from play_engine import *
from pokers.junior import Junior
import time
import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

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

table = GameTable(table_rect)
junior_poker = Junior()

engine = PlayEngine(table, junior_poker)
engine.play()


# card_anchors = find_all_in_rect(CARD_ANCHOR, table_rect)
# print(card_anchors)
