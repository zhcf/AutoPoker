from gui_element import *
from gui_control import *
from game_table import *
from play_engine import *
from pokers.junior import Junior
import time
import sys
import logging
from multiprocessing import Process, Queue

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def start_play_engine(queue, engine_code, table_rect, poker):
    table = GameTable(table_rect, queue)
    junior_poker = Junior()
    engine = PlayEngine(engine_code, table, junior_poker)
    engine.play()

if __name__=='__main__':
    game_processes = []
    queue = Queue()
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
        process = Process(target=start_play_engine, args=(queue, engine_code, table_rect, 'junior'))
        process.start()
        game_processes.append(process)

    while True:
        try:
            gui_action = queue.get(timeout=2)
            if gui_action[0] == 'click':
                click_in_rect(gui_action[1], gui_action[2])
                time.sleep(0.5)
            else:
                logging.error("Invalid GUI action: %s" % gui_action[0])
        except:
            continue
