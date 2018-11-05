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

game_engines = []
window_rects = find_all_in_screen(WINDOW_TOP_LEFT)
for window_rect in window_rects:
    window_rect.h = WINDOW_HEIGHT
    window_rect.w = WINDOW_WIDTH
    print("Game window found: %s" % window_rect.to_string())
    engine_code = '%dX%d' % (window_rect.x, window_rect.y)

    table_rect = find_in_rect(TABLE_TOP_LEFT, window_rect)
    if table_rect is None:
        print("There is no game table in window.")
        continue
    table_rect.h = TABLE_HEIGHT
    table_rect.w = TABLE_WIDTH
    print("Game table found in window: %s" % table_rect.to_string())

    table = GameTable(table_rect)
    junior_poker = Junior()

    engine = PlayEngine(engine_code, table, junior_poker)
    game_engines.append(engine)
    engine.start()

for engine in game_engines:
    engine.join()

# card_anchors = find_all_in_rect(CARD_ANCHOR, table_rect)
# print(card_anchors)
